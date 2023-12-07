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
import { Link as ReactRouterLink } from "react-router-dom";
import { Link as ChakraLink, LinkProps } from "@chakra-ui/react";
import logo from "../Assets/MusicManiaLogo.png";

const NavigationBar = () => {
  return (
    <Box bg="#22092C" position={{ sm: "sticky" }} top={0}>
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
              marginTop={"30px"}
              flexBasis={{ sm: "50%" }}
              placeholder="Buddy Search"
              borderRadius="md" // Adjust the border radius
              borderColor="teal.500" // Adjust the border color
              _focus={{
                borderColor: "teal.700", // Adjust the border color on focus
              }}
              _hover={{
                borderColor: "teal.600", // Adjust the border color on hover
              }}
              marginX={{ sm: "10px" }}
              color={"white"}
            />
            <Button
              colorScheme="green"
              marginTop={{ base: "10px", sm: "30px" }}
              flexBasis={{ sm: "20%" }}
            >
              Search!
            </Button>
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
