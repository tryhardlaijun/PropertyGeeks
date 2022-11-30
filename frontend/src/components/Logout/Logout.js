import React, {useEffect} from "react"
import { useNavigate } from "react-router-dom"
export default function Logout({isLoggedIn}){
    const navigate = useNavigate()
    useEffect(()=>{
        localStorage.removeItem('token')
        navigate("/")
    })
    return(
        <>
        </>
    )
}