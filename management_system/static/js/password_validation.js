function password_matching(password_id, cpassword_id, signup_submit, message_id) {
	let password_container = document.getElementById(password_id);
	let cpassword_container = document.getElementById(cpassword_id);
	let message_container = document.getElementById(message_id);
	console.log("message container is " + message_container);
	let message = message_container.innerHTML;
	console.log("Message is");
	console.log(message);
	let password = password_container.value;
	let cpassword = cpassword_container.value;
	let signup_submit_container = document.getElementById(signup_submit);
	signup_submit_container.disabled = true;
	
	if(password !== cpassword) {
		signup_submit_container.disabled = true;
		cpassword_container.style.border ='1px solid red';
		signup_submit_container.style.opacity ="0.4";
	}
	else if(message == ""){
		signup_submit_container.disabled = false;
		signup_submit_container.style.opacity ="1";
		cpassword_container.style.border ='1px solid green';
	}
}

function password_strength(password_id) {
	let error = "";
	let password_container = document.getElementById(password_id);
	let password = password_container.value;
	
	let re = /[a-zA-Z0-9-’/`~!#*$@_%+=.,^&(){}[\]|;:”<>?\\]/g;

	if(password.length < 5) 
		error = "Password Less than 5 characters";
	
	else if(!re.test(password))
		error = "The password must contain a letter, numeric and special character";

	return error;
}

