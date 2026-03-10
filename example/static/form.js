(function(){
    let inp_li = document.getElementsByTagName("input");
    let len = inp_li.length;
    const by_name = {};
    for(let i = 0; i < len; i++){
        inp = inp_li[i];
        by_name[inp.getAttribute("name")] = inp;
        if(inp.getAttribute("type") == "checkbox"){
            let disableName = inp.getAttribute("data-disable");
            if(disableName){
                (function(disableInput){
                    inp.onclick = function(){
                        console.log(disableInput);
                        disableInput.disabled = this.checked;
                    }
                })(by_name[disableName]);
            }
        }
    }
})();
