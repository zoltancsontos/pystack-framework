/**
 * User services javascript functionality
 * @author zoltan.csontos.dev@gmail.com
 * @version 1.0.0
 */
class UserServices {

    /**
     * Public constructor
     * @return {void}
     */
    constructor() {
        this.cookies = [];
        let signInButton = document.getElementById("sign-in");
        signInButton.addEventListener('click', e => this.signIn(e));
        this.getCookies();
    }

    getCookies() {
        this.cookies = document.cookie.split(";").map((item) => {
            var parts = item.split("=");
            return parts.length !== 0 ?
                {
                    name: parts[0],
                    value: parts[1].replace(/\"/g, '')
                } : {};
        });
    }

    /**
     * Sign in function
     * @return {void}
     */
    signIn(e) {
        e.preventDefault();
        let message = document.querySelector('.message');
        message.classList.add('hide');

        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;

        if (email === "" || password === "") {
            this.setMessage("missing email or password", "error");
        } else {
            this.sendRequest(email, password)
        }
    }

    /**
     * Sets the form message
     * @param {string} messageStr
     * @param {string} type
     */
    setMessage(messageStr, type) {
        let message = document.querySelector('.message');
        message.classList.remove('error');
        message.classList.remove('hide');
        if (type !== undefined) {
            message.innerText = messageStr;
            message.classList.add(type);
        }
    }

    /**
     * Handles the success callback
     * @param {event} e
     * @return {void}
     */
    handleCallback(e) {
        let rawData = e.srcElement.responseText;
        if (rawData !== undefined) {
            let parsedData = JSON.parse(rawData);
            if (parsedData.token !== undefined) {
                this.setMessage('You were successfully logged in!', 'success');
                if (this.cookies.length !== 0) {
                    const redirect = this.cookies.filter(item => item.name === 'redirect')[0];
                    if (redirect != undefined) {
                        setTimeout(() => {
                            window.location = redirect.value;
                        }, 1000);
                    }
                }
            } else {
                this.setMessage(parsedData.message, 'error')
            }
        }
    }

    /**
     * Sends the request to the server
     * @param {string} emailStr
     * @param {string} passwordStr
     */
    sendRequest(emailStr, passwordStr) {
        let xhr = new XMLHttpRequest();
        var data = {
            email: emailStr,
            password: passwordStr
        };
        xhr.open("POST", "/v1/users/login", true);
        xhr.addEventListener('load', e => this.handleCallback(e));
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(data));
    }
}