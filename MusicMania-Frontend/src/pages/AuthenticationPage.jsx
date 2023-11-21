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
import SignUpCard from "../components/authentication/SignUpCard";
import LoginCard from "../components/authentication/LoginCard";

const AuthenticationPage = () => {
  const history = useHistory();

  return (
    <Container maxW="xl" centerContent>
      <Box
        display="flex"
        justifyContent="center"
        w="100%"
        m="40px 0 15px 0"
        p={3}
        bg={"white"}
        borderRadius="lg"
        borderWidth="1px"
      >
        <Text fontSize="4xl" fontFamily="Poppins" color="black">
          Chatathon
        </Text>
      </Box>
      <Box
        bg="white"
        w="100%"
        p={4}
        borderRadius="lg"
        color="black"
        borderWidth="1px"
      >
        <Tabs variant="soft-rounded">
          <TabList mb="1em">
            <Tab width="50%">Login</Tab>
            <Tab width="50%">Sign up</Tab>
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

export default AuthenticationPage;
