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
} from "@chakra-ui/react";

import { SearchIcon } from "@chakra-ui/icons";

const NavigationBar = () => {
  return (
    <Box bg="#1d201f">
      <Flex justify={"space-between"}>
        <Box padding={"10px"} display={"flex"}>
          <Box pb={2} display={"flex"}>
            <Input
              placeholder="Buddy Search"
              size="md" // Adjust the size of the input (sm, md, lg)
              borderRadius="md" // Adjust the border radius
              borderColor="teal.500" // Adjust the border color
              _focus={{
                borderColor: "teal.700", // Adjust the border color on focus
              }}
              _hover={{
                borderColor: "teal.600", // Adjust the border color on hover
              }}
              marginX="10px"
              color={"white"}
            />
            <Button colorScheme="green" display={{ base: "none", sm: "flex" }}>
              Search!
            </Button>
          </Box>
        </Box>
        <Box
          marginTop="10px"
          flexBasis={"10%"}
          marginX={"5px"}
          marginBottom={"10px"}
        >
          <Menu>
            {({ isOpen }) => (
              <>
                <MenuButton as={Avatar} />
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
