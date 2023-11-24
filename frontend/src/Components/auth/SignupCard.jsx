import React, { useState } from "react";
import {
  VStack,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Button,
  useToast,
} from "@chakra-ui/react";
import { useHistory } from "react-router-dom";
import axios from "axios";

const SignUpCard = () => {
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
const history = useHistory();
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const loginSubmit = async () => {
    setLoading(true);
    if (!firstName || !lastName || !username || !email || !password || !confirmPassword) {
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

    const response = await fetch("/api/auth/signup", {headers: new Headers({'content-type': 'application/json'}), method: "POST", body: JSON.stringify({"first-name": firstName, "last-name": lastName, "user-name": username, "email": email, "password": password, "confirm-password": confirmPassword})});
    const data = await response.json()
    

    if (!response.ok) {
      throw new Error(`${data.error}`);
    }
      history.push("/home");
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
    <VStack spacing="5px" color="black">
      <FormControl id="firstName" isRequired>
        <FormLabel color={"#F05941"}>First Name</FormLabel>
        <Input
          placeholder="Enter Your First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          color={"white"}
        />
      </FormControl>
      <FormControl id="lastName" isRequired>
        <FormLabel color={"#F05941"}>Last Name</FormLabel>
        <Input
          placeholder="Enter Your Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          color={"white"}
        />
      </FormControl>
      <FormControl id="username" isRequired>
        <FormLabel color={"#F05941"}>Username</FormLabel>
        <Input
          placeholder="Enter Your Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          color={"white"}
        />
      </FormControl>
      <FormControl id="email" isRequired>
        <FormLabel color={"#F05941"}>Email</FormLabel>
        <Input
          placeholder="Enter Your Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
            <FormControl id="confirm-password" isRequired>
        <FormLabel color={"#F05941"}>Confirm Password</FormLabel>
        <InputGroup>
          <Input
            type={show ? "text" : "password"}
            placeholder="Enter Your Password Again"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
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
        onClick={loginSubmit}
        _hover={{bg: "#F05941"}}
      >
        Signup
      </Button>
    </VStack>
  );
};

export default SignUpCard;
