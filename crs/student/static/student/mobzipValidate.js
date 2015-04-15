        function Validate(inputText1,inputText2)  
    	{  

            var mob = /[0-9]{10}/;  
            var pin = /[0-9]{6}/; 
            if(inputText1.value.match(mob))  
            {  
                document.test.mobile.focus();
                if(inputText2.value.match(pin))  
                {  
                    document.test.pincode.focus();  
                    return true;  
                }  
                else
                {  
                    alert("You have entered an invalid Zip Code!");  
                    document.test.pincode.focus();  
                    return false;  
                }  
            }  
            else  
            {  
                alert("You have entered an invalid Mobile Number!");  
                document.test.mnum.focus();  
                return false;  
            }  
        }



  
