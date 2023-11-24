import React from 'react'
import NavigationBar from "../Components/NavigationBar"
import { useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { Text, useToast } from '@chakra-ui/react'



const EmailConfimrationPage = () => {
    const location = useLocation()
    const toast = useToast()

    useEffect(() => {
        const sendEmail = async () => {
            const queryParameters = new URLSearchParams(location.search)
            const token = queryParameters.get("auth")

            try {
                const confirmationResponse = await fetch(`/api/auth/confirm/${token}`, {headers: new Headers({'content-type': 'application/json'}), method: "PUT"});
                const confirmationResponseData = await confirmationResponse.json()
            
                if (!confirmationResponse.ok) {
                    throw new Error(`${confirmationResponseData.error}`)
                }

                toast({
                    title: "Successfully Confirmed Email! Click Logo to return to Homepage",
                    status: "success",
                    isClosable: true,
                    position: "bottom",
                });
            } catch (error) {
                toast({
                    title: "Error Occured!!",
                    status: "error",
                    description: error.message,
                    duration: 5000,
                    isClosable: true,
                    position: "bottom",
                });
            }
        }

        sendEmail()

    })
  return (
    <>

    </>
    )
}

export default EmailConfimrationPage