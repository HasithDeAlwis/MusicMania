import React, { useState, useEffect } from "react";
import {
  Flex,
  Box,
  Container,
  Text,
  Button,
  Avatar,
  Input,
  Menu,
  MenuItem,
  MenuList,
  MenuButton,
  IconButton,
  Image,
} from "@chakra-ui/react";
import { useHistory } from "react-router-dom";
import { Link as ReactRouterLink } from "react-router-dom";
import { PhoneIcon, QuestionIcon } from "@chakra-ui/icons";
import { Link as ChakraLink, Tooltip, useToast } from "@chakra-ui/react";
import logo from "../Assets/MusicManiaLogo.png";

const NavigationBar = () => {
  const toast = useToast();
  const [isDropdownOpen, setDropdownOpen] = useState(true);
  const [searchTerm, setSearchTerm] = useState();
  const [profile, setProfile] = useState();
  const history = useHistory();
  const parseSearch = () => {
    //replace all the ' ' in the search to a '+'
  };
  //handle the users search request
  const handleSearch = () => {
    const searchQuerry = searchTerm.replaceAll(" ", "+");
    history.push(`/search?search-term=${searchQuerry}`);
  };

  useEffect(() => {
    const getProfile = async () => {
      try {
        //Make call to get the spotify api to get the users top songs
        const profileResponse = await fetch(
          `/api/spotify/get-profile-picture`,
          {
            headers: new Headers({ "content-type": "application/json" }),
            method: "GET",
          }
        );
        const profileData = await profileResponse.json();
        const data = await profileData;
        setProfile(() => {
          return data["profile-picture"];
        });
        if (!profileResponse.ok) {
          throw new Error(`${profileData.error}`);
        }

        console.log(data);
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
    };

    getProfile();
  }, []);

  return (
    <Box bg="#22092C" position={{ sm: "sticky" }} top={0} zIndex={2}>
      <Flex justify={{ base: "center", sm: "space-between" }}>
        <Box padding={"10px"} display={"flex"}>
          <Box
            pb={2}
            display={"flex"}
            justifyContent={{ base: "center", sm: "start" }}
            flexDir={{ base: "column", sm: "row" }}
            wrap={{ base: "nowrap", md: "wrap" }}
          >
            <Box maxW="200px" maxH="200px">
              <ChakraLink as={ReactRouterLink} to={"/profile"}>
                <Image src={logo} alt="Logo" />
              </ChakraLink>
            </Box>

            <Input
              placeholder="Buddy Search"
              borderRadius="md" // Adjust the border radius
              borderColor="teal.500" // Adjust the border color
              _focus={{
                borderColor: "teal.700", // Adjust the border color on focus
              }}
              _hover={{
                borderColor: "teal.600", // Adjust the border color on hover
              }}
              color={"white"}
              onChange={(e) => setSearchTerm(e.target.value)}
              value={searchTerm}
              marginTop={{ sm: "30px" }}
              marginX={2}
            />
            <Box display="flex" flexBasis={{ sm: "50%" }}>
              <Button
                marginTop={{ base: "10px", sm: "30px" }}
                flexBasis={{ base: "90%" }}
                colorScheme="green"
                justifySelf={"start"}
                marginLeft={{ base: 5, sm: 0 }}
                onClick={handleSearch}
              >
                Search!
              </Button>
              <Tooltip label="Enter artists or songs you like seperated by commas to find users of similar taste!">
                <QuestionIcon
                  color={"#BE3144"}
                  boxSize={8}
                  marginTop={{ base: "10px", sm: "33px" }}
                  marginLeft={{ base: 4, sm: 3 }}
                  display={{ base: "none", sm: "block" }}
                />
              </Tooltip>
            </Box>
          </Box>
        </Box>
        <Box
          marginTop="25px"
          flexBasis={"10%"}
          marginBottom={"10px"}
          marginLeft={{ base: "5px", sm: "0" }}
        >
          {profile && (
            <Menu>
              {({ isOpen }) => (
                <>
                  <MenuButton
                    as={Avatar}
                    boxSize={{ base: "2.5em", sm: "3em" }}
                    src={profile}
                  />
                  <MenuList>
                    <MenuItem>Profile</MenuItem>
                    <MenuItem
                      onClick={() => {
                        history.push("/authenticate");
                      }}
                    >
                      Logout
                    </MenuItem>
                  </MenuList>
                </>
              )}
            </Menu>
          )}
        </Box>
      </Flex>
    </Box>
  );
};

export default NavigationBar;
