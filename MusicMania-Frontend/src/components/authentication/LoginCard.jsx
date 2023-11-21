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
          "Content-Type": "application/json; charset=utf-8.",
        },
      };

      const params = { identifier: identifier, password: password };
      const { data } = await axios.get(
        "/api/auth/login", 
        {identifier, password},
        config
      );

      toast({
        title: "Login Successful",
        status: "success",
        duration: 5000,
        isClosable: true,
        position: "bottom",
      });
      history.push("/home");
      return;
    } catch (error) {
      toast({
        title: "Error Occured!!",
        status: "error",
        description: error.response.data.message,
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
        <FormLabel>Email or Username</FormLabel>
        <Input
          placeholder="Enter Your Email or Username"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
        />
      </FormControl>
      <FormControl id="password" isRequired>
        <FormLabel>Password</FormLabel>
        <InputGroup>
          <Input
            type={show ? "text" : "password"}
            placeholder="Enter Your Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
        colorScheme="blue"
        width="100%"
        isLoading={loading}
        style={{ marginTop: 15 }}
        onClick={loginHandler}
      >
        Login
      </Button>
    </VStack>
  );
};

export default LoginCard;
