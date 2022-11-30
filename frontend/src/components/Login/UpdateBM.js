import { React, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

function UpdateBM(){
	const [newDesc, setNewDesc] = useState("")
    const params = useParams();
	console.log(params);
    var bodyFormData = new FormData();
	bodyFormData.append("UserID", params.uid);
    bodyFormData.append("bookmark_id", 1);
    let URI = "http://127.0.0.1:5000/view/updateBookmark";
    async function updatemark() {
        try {
            bodyFormData.append("description", newDesc);
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
    return (
		<div>
            <label>Description: </label>
            <input type="text" value= {newDesc} onChange={(e)=>{setNewDesc(e.target.value)}}>

            </input>
            <button onClick={updatemark}>
                Update This
            </button>
		</div>
	);
};

export default UpdateBM;
