(function(){
    if(typeof window._polyvinyl === "undefined"){
        window._polyvinyl = {}
    }

    if(typeof window._polyvinyl.form !== "undefined"){
        return;
    }

    let inp_li = document.getElementsByTagName("input");
    let len = inp_li.length;
    const by_name = {};
    for(let i = 0; i < len; i++){
        inp = inp_li[i];
        by_name[inp.getAttribute("name")] = inp;
    } 

    for(let i = 0; i < len; i++){
        inp = inp_li[i];
        if(inp.getAttribute("type") == "checkbox"){
            let disableName = inp.getAttribute("data-disable");
            if(disableName){
                (function(disableInput){
                    inp.onclick = function(){
                        disableInput.disabled = this.checked;
                        console.log(disableInput);
                    }
                })(by_name[disableName]);
            }
        }
    }

    function _validateRules(content, rules){
        let i = 0;
        for(; i < rules.length; i++){
            const re = rules[i];
            if(re && !re.test(content)){
                return i;
            }
        }
        if(i == rules.length){
            return -1;
        }
    }

    function validatePartially(e){
        if(this._validation){
            if(this.parentNode.classList.contains("invalid")){
                validateFully.call(this, e);
            }else{
                const broke = _validateRules(this.value, this._val.rules);
                if(broke === -1){
                    this.parentNode.classList.add("valid");
                    this.parentNode.classList.remove("invalid");
                    this._valid = true
                    this._validation.validate();
                }else{
                    this.parentNode.classList.remove("valid");
                    this._valid = false;
                    this._validation.validate();
                }
            }
        }
    }

    function validateFully(e){
        if(this._val && this._val.rules){
            const broke = _validateRules(this.value, this._val.rules);
            if(broke === -1){
                this.parentNode.classList.add("valid");
                this.parentNode.classList.remove("invalid");
                this._valid = true;
                this._validation.validate();
            }else{
                this.parentNode.classList.remove("valid");
                this.parentNode.classList.add("invalid");
                this._valid = false;
                this._validation.validate();
                if(this._desc_el){
                    const length = this._desc_el.childNodes.length;
                    for(let i = 0; i < length; i++){
                        const desc = this._desc_el.childNodes.item(i);
                        if(i == broke){
                            desc.classList.add("broken"); 
                        }else{
                            desc.classList.remove("broken"); 
                        }
                    }
                }
            }
        }else{
            if(this.value || this.checked){
                this._valid = true;
                this._validation.validate();
            }
        }
    }

    function validateLast(e){
        if(this._validation && typeof this._validation.form._latest !== "undefined" && this._validation.form._latest !== this){
            validateFully.call(this._validation.form._latest, e);
        }
        this._validation.form._latest = this;
    }

    function validateValue(e){
        validateLast.call(this, e);
        if(this.value || this.checked){
            this._valid = true;
            this._validation.validate();
        }else if(this._required){
            this._valid = false;
            if(this._desc_el){
                const length = this._desc_el.childNodes.length;
                for(let i = 0; i < length; i++){
                    const desc = this._desc_el.childNodes.item(i);
                    if(i == broke){
                        desc.classList.add("broken"); 
                    }else{
                        desc.classList.remove("broken"); 
                    }
                }
            }
            this._validation.validate();
        }
    }


    function validateButton(e){
       validateLast.call(this, e); 
       if(!this._valid){
            e.stopPropagation();
            e.preventDefault();
            return false;
       }
    }

    function validate(){
        let i = 0;
        for(; i < this.elems.length; i++){
            const el = this.elems[i];
            visible = el.getBoundingClientRect().height > 0;
            console.log("required " + el._required+" visible "+visible+" valid "+el._valid, el);
            if(el._required && visible && !el._valid){
                break;
            }
        }
        const valid = i === this.elems.length;
        let cls = "invalid";
        let oldCls = "valid";
        if(valid){
            cls = "valid";
            oldCls = "invalid";
        }
        for(let i = 0; i < this.buttons.length; i++){
            this.buttons[i]._valid = valid;
            this.buttons[i].classList.add(cls);
            this.buttons[i].classList.remove(oldCls);
        }
    }

    function register(jsid, validation){
         validation.form = document.getElementById(jsid);
         validation.elems = [];
         validation.buttons = [];
         validation.validate = validate;
         validation._valid = false;
         this.elems[jsid] = {
              validation,
         }

         const buttons = validation.form.getElementsByTagName("BUTTON");
         let l = buttons.length;
         for(let i = 0; i < l; i++){
              const btn = buttons[i];
              btn.addEventListener("click", validateButton);
              btn._validation = validation;
              btn._valid = false;
              validation.buttons.push(btn);
         }

         const inputs = validation.form.getElementsByTagName("INPUT");
         l = inputs.length;
         for(let i = 0; i < l; i++){
              const inp = inputs[i];
              validation.elems.push(inp);

              inp._validation = validation;
              inp._valid = false;
              inp.addEventListener("focus",validateLast);
              inp.addEventListener("click",validateLast);

              const name = inp.getAttribute("name");
              if(validation[name]){
                  val = validation[name];
                  if(val.rules){
                      for(let ii = 0; ii < val.rules.length; ii++){
                          if(val.rules[ii]){
                              val.rules[ii] = new RegExp(val.rules[ii]);
                          }
                      }
                      inp.addEventListener("keyup", validatePartially);
                  }else{
                      inp.addEventListener("keyup", validateValue);
                  }

                  if(val.description){
                      const desc = document.createElement("P");
                      for(let ii = 0; ii < val.description.length; ii++){
                          const part = document.createElement("SPAN");
                          part.append(document.createTextNode(val.description[ii]));
                          desc.append(part);
                      }
                      desc.classList.add("val-description");
                      inp.parentNode.after(desc);
                      inp._desc_el = desc;
                  }
                  inp._val = val;
                  inp._required = true;
              }else{
                  inp._required = false;
              }

              if(inp.getAttribute("type") === "password"){
                    let node = inp;
                    while(node){
                        node = node.nextSibling; 
                        if(node && node.classList.contains("eye")){
                            (function(pwinp){
                                node.onclick = function(){
                                    console.log("Oop");
                                    if(pwinp.classList.contains("visible-password")){
                                        pwinp.classList.remove("visible-password");
                                        this.classList.remove("active");
                                        pwinp.setAttribute("type", "password");
                                    }else{
                                        pwinp.classList.add("visible-password");
                                        this.classList.add("active");
                                        pwinp.setAttribute("type", "text");
                                    }
                                }
                            })(inp);
                        }
                    }
              }

              if(inp.value){
                   validateFully.call(inp, null)
              }
         }
         validation.validate(validation._valid);
    }

    window._polyvinyl.form = {
        register,
        elems: {}
    }

})();
