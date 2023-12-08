import React, { useEffect, useState } from "react";
import { Flex, Box, Text, Image, VStack, Link } from "@chakra-ui/react";
import spotify from "../profile/assets/spotify.svg";
import NoImageFound from "../profile/assets/NoImageFound.jpeg";
const PlaylistColumn = (props) => {
  const [song, setSong] = useState();

  useEffect(() => {
    return setSong(() => {
      return props.song;
    });
  });
  return (
    <>
      {song && (
        <Flex
          justify={"start"}
          bg={"#22092C"}
          _hover={{
            textDecoration: "underline",
            cursor: "pointer",
            boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
          }}
          boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
          transition={"200ms"}
          marginBottom={2}
        >
          <Box
            width={"50px"} // Set the size of the square box
            height={"50px"}
          >
            {song.image != "" ? (
              <Image
                src={song.image}
                objectFit={"cover"}
                width={"100%"}
                height={"100%"}
                alt={`Song cover for ${song.title}`}
              ></Image>
            ) : (
              <Image
                src={NoImageFound}
                objectFit={"cover"}
                width={"100%"}
                height={"100%"}
                alt={`Song cover for ${song.title}`}
              ></Image>
            )}
          </Box>
          <VStack>
            <Box alignSelf={"start"}>
              <Text
                marginLeft={2}
                fontFamily={"Poppins"}
                fontSize={"15px"}
                fontWeight={900}
                color={"white"}
              >
                {song.title}
              </Text>
            </Box>

            <Flex alignSelf="start">
              {song.artist.map((creator, index) => (
                <Box marginLeft={2} key={index}>
                  {index == 0 ? (
                    <Text
                      color={"white"}
                      fontFamily={"Poppins"}
                      fontSize={"15px"}
                    >
                      {creator}
                    </Text>
                  ) : (
                    <Text
                      colorScheme={"#000000"}
                      fontFamily={"Poppins"}
                      fontSize={"15px"}
                    >
                      & {creator}
                    </Text>
                  )}
                </Box>
              ))}
            </Flex>
          </VStack>
          <Link ml={"auto"} href={song.link}>
            <Box>
              <Image src={spotify}></Image>
            </Box>
          </Link>
        </Flex>
      )}
    </>
  );
};

export default PlaylistColumn;
