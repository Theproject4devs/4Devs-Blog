
        function toggleDisplaySignUp() {
            var formSignUp = document.getElementById('fncSignup');
            var formSignIn = document.getElementById('fncSignin');
            formSignUp.style.display = 'flex';
            formSignIn.style.display = 'none';
        }

        function toggleDisplaySignIn() {
            var formSignUp = document.getElementById('fncSignup');
            var formSignIn = document.getElementById('fncSignin');
            formSignUp.style.display = 'none';
            formSignIn.style.display = 'flex';
        }