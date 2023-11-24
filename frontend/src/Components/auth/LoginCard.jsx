import React, { useState } from "react";
import {
  FormControl,
  FormLabel,
  VStack,
  Input,
  InputGroup,
  InputRightElement,
  Button,
  useToast,
} from "@chakra-ui/react";
import { useHistory } from "react-router-dom";
import axios from "axios";

const LoginCard = () => {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const history = useHistory();

  const loginHandler = async () => {
    setLoading(true);
    if (!identifier || !password) {
      toast({
        title: "Please Fill all the Fields",
        status: "warning",
        duration: 5000,
        isClosable: true,
        position: "bottom",
      });
      setLoading(false);
      return;
    }

    try {
      const config = {
        headers: {
          "Content-Type": "application/json",
        },
      };

      //const params = { identifier: identifier, password: password };
      const response = await fetch("/api/auth/login", {headers: new Headers({'content-type': 'application/json'}), method: "POST", body: JSON.stringify({"identifier": identifier, "password": password})}  );
      const data = await response.json()

      if (!response.ok) {
        throw new Error(`${data.error}`);
      }
      //const {data} = await axios.get("/api/auth/login", config, {identifier, password})
      toast({
        title: "Login Successful",
        status: "success",
        duration: 5000,
        isClosable: true,
        position: "bottom",
      });
      
      const spotifyResponse = await fetch("/api/spotify/authenticate", {headers: new Headers({'content-type': 'application/json'}), method: "GET"});
      const spotifyData = await spotifyResponse.json()
      
      //const spotifyRedirect = await fetch(spotifyData.url)

      window.location.href = spotifyData.url;
    } catch (error) {
      toast({
        title: "Error Occured!!",
        status: "error",
        description: error.message,
        duration: 5000,
        isClosable: true,
        position: "bottom",
      });
      setLoading(false);
      return;
    }
  };

  return (
    <VStack spacing="5px" color="back">
      <FormControl id="email" isRequired>
        <FormLabel color={"#F05941"}>Email or Username</FormLabel>
        <Input
          placeholder="Enter Your Email or Username"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          color={"white"}
        />
      </FormControl>
      <FormControl id="password" isRequired>
        <FormLabel color={"#F05941"}>Password</FormLabel>
        <InputGroup>
          <Input
            type={show ? "text" : "password"}
            placeholder="Enter Your Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            color={"white"}
          />
          <InputRightElement width="4.5rem">
            <Button
              h="1.75rem"
              size="sm"
              onClick={() => setShow((prevShow) => !prevShow)}
            >
              {show ? "Hide" : "Show"}
            </Button>
          </InputRightElement>
        </InputGroup>
      </FormControl>
      <Button
        bg="#BE3144"
        width="100%"
        isLoading={loading}
        style={{ marginTop: 15 }}
        onClick={loginHandler}
        _hover={{bg: "#F05941"}}
      >
        Login
      </Button>
    </VStack>
  );
};

export default LoginCard;
