import React, { useState } from "react";
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
import { Link as ChakraLink, LinkProps } from "@chakra-ui/react";
import logo from "../Assets/MusicManiaLogo.png";

const NavigationBar = () => {
  const [isDropdownOpen, setDropdownOpen] = useState(true);
  const [searchTerm, setSearchTerm] = useState();
  const history = useHistory();
  const parseSearch = () => {
    //replace all the ' ' in the search to a '+'
  };
  //handle the users search request
  const handleSearch = () => {
    const searchQuerry = searchTerm.replaceAll(" ", "+");
    history.push(`/search?search-term=${searchQuerry}`);
  };

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
            <Button
              marginTop={{ base: "10px", sm: "30px" }}
              flexBasis={{ sm: "50%" }}
              order={2}
              colorScheme="green"
              justifySelf={"start"}
              marginLeft={{ base: 4, sm: 0 }}
              onClick={handleSearch}
            >
              Search!
            </Button>

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
          </Box>
        </Box>
        <Box
          marginTop="25px"
          flexBasis={"10%"}
          marginBottom={"10px"}
          marginLeft={{ base: "5px", sm: "0" }}
        >
          <Menu>
            {({ isOpen }) => (
              <>
                <MenuButton
                  as={Avatar}
                  boxSize={{ base: "2.5em", sm: "3em" }}
                />
                <MenuList>
                  <MenuItem>Profile</MenuItem>
                  <MenuItem>Playlist</MenuItem>
                  <MenuItem>Logout</MenuItem>
                </MenuList>
              </>
            )}
          </Menu>
        </Box>
      </Flex>
    </Box>
  );
};

export default NavigationBar;
