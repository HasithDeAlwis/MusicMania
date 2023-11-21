import { useEffect } from "react";
import {
  Container,
  Box,
  Text,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";
import React from "react";
import { useHistory } from "react-router-dom";
import SignUpCard from "../Components/auth/SignupCard";
import LoginCard from "../Components/auth/LoginCard";

const SignUpLoginPage = () => {
  const history = useHistory();

  return (

    <Container maxW="xl" centerContent>
      <Box
      marginTop={"10px"}
        bg={"#22092C"}
        w="100%"
        p={4}
        borderRadius="lg"
        color="black"
        borderWidth="1px"
      >
        <Tabs variant="soft-rounded">
          <TabList mb="1em">
            <Tab width="50%" bg={"white"} color={"#22092C"} margin={"2px"}>Login</Tab>
            <Tab width="50%" bg={"white"} color={"#22092C"} margin={"2px"}>Sign up</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <LoginCard />
            </TabPanel>
            <TabPanel>
              <SignUpCard />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </Container>
  );
};

export default SignUpLoginPage;