import React from "react";
import ResetPassword from "../components/regions/ResetPassword/Presentation";
import user from "./fixtures/user.json";


export default {
    title: "Tilde/ResetPassword",
    component: ResetPassword
}

export const Primary = () => <ResetPassword email={user.email}/>