import { React, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

function DelBM(){
    const params = useParams();
	console.log(params);
    var bodyFormData = new FormData();
	bodyFormData.append("UserID", params.uid);
    bodyFormData.append("bookmark_id", params.bid);
    var navigate = useNavigate()
    let URI = "http://127.0.0.1:5000/view/deleteBookmark";
    async function delmark() {
        try {
            const response = await axios({
                method: "post",
                url: URI,
                data: bodyFormData,
                headers: { "Content-Type": "multipart/form-data" },
            });
            console.log(response.data);
        } catch (error) {
            const message = `An error occurred: ${error}`;
            console.log(message);
            return;
        }
    }
    useEffect(() => {
      delmark().then(()=>{
        navigate("/profile")
      })
      return;
    })
    
    return (
        <></>
	);
};

export default DelBM;
