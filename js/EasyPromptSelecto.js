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
        max-height: 200px;
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
async function getPrompt(name) {
    if(pb_cache[name])
		return pb_cache[name];
	else {
        const resp = await api.fetchApi(`/lam/getPrompt?name=${name}`);
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
    Object.keys(tags).forEach((k) => {
        if (typeof tags[k] === "string") {
            let t=[k, tags[k]]
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
                        textContent: t[1],
                    }),
                ]
            ))
        }else{
            rlist.push(...getTagList(tags[k]))
        }
    });
    return rlist
}
// Displays input text on a node
app.registerExtension({
    name: "EasyPromptSelecto",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
		var names=['EasyPromptSelecto']
        if (names.indexOf(nodeData.name)>=0) {
            // When the node is created we want to add a readonly text widget to display the text
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function() {
                const r = onNodeCreated?.apply(this, arguments);
                ComfyWidgets["COMBO"](this, "category", ['a','b']).widget;
                const list = $el("ol.lam-model-tags-list",[]);
                let tags=this.addDOMWidget('tags',"list",list)
                let prompt_type = this.widgets[this.widgets.findIndex(obj => obj.name === 'prompt_type')];
                let textEl = this.widgets[this.widgets.findIndex(obj => obj.name === 'text')];
                let category = this.widgets[this.widgets.findIndex(obj => obj.name === 'category')];
                let cat_values=[]
                let cat_value=''
                Object.defineProperty(category.options, "values", {
                    set: (x) => {
                    },
                    get: () => {
                        getPrompt(prompt_type.value);
                        if(pb_cache[prompt_type.value] == undefined) {
                            return cat_values;
                        }
                        if(cat_values.join(',')!=Object.keys(pb_cache[prompt_type.value]).join(',')){
                            cat_values=Object.keys(pb_cache[prompt_type.value])
                            cat_value=''
                        }
                        return cat_values;
                    }
                });
                Object.defineProperty(category, "value", {
                    set: (x) => {
                        if(cat_value!=x){
                            cat_value=x;
                            if(!cat_value){
                                return 
                            }
                            let textvalue=textEl.value
                            if(this.widgets.length!=4){
                                const list = $el("ol.lam-model-tags-list", getTagList(pb_cache[prompt_type.value][cat_value]));
                                this.addDOMWidget('tags',"list",list)
                            }else{
                                if(pb_cache[prompt_type.value]&&pb_cache[prompt_type.value][cat_value]){
                                    this.widgets[3].element.innerHTML=''
                                    let list =getTagList(pb_cache[prompt_type.value][cat_value]);
                                    this.widgets[3].element.append(...list)
                                }
                            }
                            this.widgets[3].element.querySelectorAll(".lam-model-tag").forEach(el => {
                                if(textvalue.indexOf(el.dataset.tag)!==-1){
                                    el.classList.add("lam-model-tag--selected");
                                }
                            });
                            
                        }
                    },
                    get: () => {
                        return cat_value;
                    }
                });
                let text_value=''
               
                Object.defineProperty(tags, "value", {
                    set: (x) => {
                        
                    },
                    get: () => {
                        this.widgets[3].element.querySelectorAll(".lam-model-tag").forEach(el => {
                            if(el.classList.value.indexOf("lam-model-tag--selected")>=0){
                                if(textEl.value.indexOf(el.dataset.tag)===-1){
                                    textEl.value+=(textEl.value&&textEl.value[textEl.value.length-1]===',')?el.dataset.tag+',':','+el.dataset.tag+',';
                                }
                            }else{
                                if(textEl.value.indexOf(el.dataset.tag)!==-1&&textEl.value.indexOf(','+el.dataset.tag)!==-1
                                &&textEl.value.indexOf(el.dataset.tag+',')!==-1
                                ){
                                    textEl.value=textEl.value.replace(el.dataset.tag+',','');
                                }
                            }
                            
                        });
                        return '';
                    }
                });
                this.setSize([400, 400]);
                return r;
            };

        }
    },
});