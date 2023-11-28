import { app } from "/scripts/app.js";
import { $el } from "../../../scripts/ui.js";
import { ComfyWidgets } from "/scripts/widgets.js";
import { api } from "../../../scripts/api.js";

$el("style", {
	textContent: `
    .lam-model-info {
        color: white;
        font-family: sans-serif;
        max-width: 90vw;
    }
    .lam-model-content {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    .lam-model-info h2 {
        text-align: center;
        margin: 0 0 10px 0;
    }
    .lam-model-info p {
        margin: 5px 0;
    }
    .lam-model-info a {
        color: dodgerblue;
    }
    .lam-model-info a:hover {
        text-decoration: underline;
    }
    .lam-model-tags-list {
        display: flex;
        flex-wrap: wrap;
        list-style: none;
        gap: 10px;
        min-height: 100px;
        max-height: 400px;
        overflow: auto;
        margin: 10px 0;
        padding: 0;
    }
    .lam-model-tag {
        background-color: rgb(128, 213, 247);
        color: #000;
        display: flex;
        align-items: center;
        gap: 5px;
        border-radius: 5px;
        padding: 2px 5px;
        cursor: pointer;
    }
    .lam-model-tag--selected span::before {
        content: "✅";
        position: absolute;
        background-color: dodgerblue;
        top: 0;
        right: 0;
        bottom: 0;
        text-align: center;
    }
    .lam-model-tag:hover {
        outline: 2px solid dodgerblue;
    }
    .lam-model-tag p {
        margin: 0;
    }
    .lam-model-tag span {
        text-align: center;
        border-radius: 5px;
        background-color: dodgerblue;
        color: #fff;
        padding: 2px;
        position: relative;
        min-width: 20px;
        overflow: hidden;
    }
    
    .lam-model-metadata .comfy-modal-content {
        max-width: 100%;
    }
    .lam-model-metadata label {
        margin-right: 1ch;
        color: #ccc;
    }
    
    .lam-model-metadata span {
        color: dodgerblue;
    }
    
    .lam-preview {
        max-width: 50%;
        margin-left: 10px;
        position: relative;
    }
    .lam-preview img {
        max-height: 300px;
    }
    .lam-preview button {
        position: absolute;
        font-size: 12px;
        bottom: 10px;
        right: 10px;
    }
    .lam-model-notes {
        background-color: rgba(0, 0, 0, 0.25);
        padding: 5px;
        margin-top: 5px;
    }
    .lam-model-notes:empty {
        display: none;
    }    

`,
parent: document.body,
})

let pb_cache = {};
async function getStyles(name) {
    if(pb_cache[name])
		return pb_cache[name];
	else {
        const resp = await api.fetchApi(`/lam/getStyles?name=${name}`);
        if (resp.status === 200) {
            let data = await resp.json();
            pb_cache[name] = data;
            return data;
        }
        return undefined;
    }
    
}
function getTagList(tags) {
    let rlist=[]
    tags.forEach((k,i) => {
        let t=[ k['zhName'],k['name']]
        rlist.push($el(
            "li.lam-model-tag",
            {
                dataset: {
                    tag: t[1],
                },
                $: (el) => {
                    el.onclick = () => {
                        el.classList.toggle("lam-model-tag--selected");
                    };
                },
            },
            [
                $el("p", {
                    textContent: t[0],
                }),
                $el("span", {
                    textContent: i,
                }),
            ]
        ))
    });
    return rlist
}
// Displays input text on a node
app.registerExtension({
    name: "StyleSelecto",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=['StyleSelecto']
        if (names.indexOf(nodeData.name)>=0) {
            // When the node is created we want to add a readonly text widget to display the text
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                let style_type = this.widgets[this.widgets.findIndex(obj => obj.name === 'style_type')];
                this.setProperty("values", [])
                //stylesEl.inputEl.classList.add("lam-model-notes");
                const list = $el("ol.lam-model-tags-list",[]);
                let styles=this.addDOMWidget('styles',"list",list)
                let st_values=''
                Object.defineProperty(style_type, "value", {
                    set: (x) => {
                        st_values=x
                        if(st_values){
                            getStyles(st_values);
                            styles.element.innerHTML=''
                            if(pb_cache[st_values]){
                                    let list =getTagList(pb_cache[st_values]);
                                    styles.element.append(...list)
                                    styles.element.querySelectorAll(".lam-model-tag").forEach(el => {
                                    if(this.properties["values"].includes(el.dataset.tag)){
                                        el.classList.add("lam-model-tag--selected");
                                    }
                                    this.setSize([500, 400]);
                                });
                            }
                            
                        }
                    },
                    get: () => {
                        if(pb_cache[st_values]&&styles.element.children.length==0){
                                let list =getTagList(pb_cache[st_values]);
                                styles.element.append(...list)
                                styles.element.querySelectorAll(".lam-model-tag").forEach(el => {
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    el.classList.add("lam-model-tag--selected");
                                }
                                this.setSize([500, 400]);
                            });
                        }
                        return st_values;
                    }
                });
                let stylesValue=''
                Object.defineProperty(styles, "value", {
                    set: (x) => {
                        
                    },
                    get: () => {
                            styles.element.querySelectorAll(".lam-model-tag").forEach(el => {
                            if(el.classList.value.indexOf("lam-model-tag--selected")>=0){
                                if(!this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"].push(el.dataset.tag);
                                    stylesValue = this.properties["values"].join(',');
                                }
                            }else{
                                if(this.properties["values"].includes(el.dataset.tag)){
                                    this.properties["values"]=this.properties["values"].filter(v=>v!=el.dataset.tag);
                                    stylesValue = this.properties["values"].join(',');
                                }
                            }
                            
                        });
                        return stylesValue;
                    }
                });
                
                this.setSize([500, 400]);
                return r;
            };

        }
    },
});