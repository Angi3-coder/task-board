import React, { useState } from 'react'

function Signup() {
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [message, setMessage] = useState('')

  
    async function handleSignUp(e){
        e.preventDefault();

        const response = await fetch('http://127.0.0.1:8000/signup', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username, email, password
            })
        })
        const data = await response.json()

        if (response.ok){
            setMessage(data.message);
            setUsername('');
            setEmail('');
            setPassword('');
        } else {
            setMessage(data.error)
        }
    }

  return (
    <div>
      <h1>Sign up</h1>
      <form onSubmit={handleSignUp}>
        <input type='text' name='username' value={username} onChange={e=>setUsername(e.target.value)}  placeholder='username'/>
        <input type='email' name='email' value={email} onChange={e=>setEmail(e.target.value)}  placeholder='name@example.com'/>
        <input type='password' name='password' value={password} onChange={e=>setPassword(e.target.value)}  placeholder='password'/>

        <button>Sign Up</button>
      </form>
      <p>{message}</p>

    </div>
  )
}

export default Signup
