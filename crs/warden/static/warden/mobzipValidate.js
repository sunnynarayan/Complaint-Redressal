        function Validate(inputText1,inputText2)  
    	{  
    		ValidateMobile(inputText1);
    		ValidateZip(inputText2)
        	
    	}  

    	function ValidateMobile(inputText)
    	{
    		var mob = /[0-9]{10}/;  
        	if(inputText.value.match(mob))  
        	{  
            	document.test.mnum.focus();  
            	return true;  
        	}  
        	else  
        	{  
            	alert("You have entered an invalid Mobile Number!");  
            	document.test.mnum.focus();  
            	return false;  
        	}  
    	}

    	function ValidateZip(inputText)
    	{
    		var mob = /[0-9]{6}/;  
        	if(inputText.value.match(mob))  
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
