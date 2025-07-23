export default {
    template: `
        <div class="row border">
            <div class="col" style="height: 750px;">
                <div class="border mx-auto mt-5" style="height: 400px; width: 300px">
                    <div>
                        <h2 class="text-center">Login Form</h2>
                        <div>
                            <label for="email">Enter your email:</label>
                            <input type="text" id="email" v-model="email">
                        </div>
                        <div>
                            <label for="email">Enter your password:</label>
                            <input type="password" id="pass" v-model="password">
                        </div>
                        <div>
                            <button @click="loginUser" class="btn btn-primary">Login</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    data: function(){
        return {
            formData : {
                email: "",
                password: ""
            }
        }
    },

    methods: {
        loginUser: function() {
            fetch('/api/login', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.formData) // this content goes to backend as JSON data
            })
            .then(response => response.json())
            .then(data =>{
                localStorage.setItem("auth-token", data["auth-token"])
                localStorage.setItem("id", data.id)
                this.$router.push('/dashboard') // redirect to home page
            })
        }
    }
}