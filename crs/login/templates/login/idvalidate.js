    function ValidateEmail(inputText)  
    {  
        var mailformat = /(^\w+([\.]\w+)@+(stud)+$)|(^\w+@+(fac)+$)/;  
        if(inputText.value.match(mailformat))  
        {  
            document.form1.userName.focus();  
            return true;  
        }  
        else  
        {  
            alert("You have entered an invalid email address!");  
            document.form1.userName.focus();  
            return false;  
        }  
    }  