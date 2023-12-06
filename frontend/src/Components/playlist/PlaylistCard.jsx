import React, { useEffect, useState } from "react";
import { Image, Text, Box, VStack } from "@chakra-ui/react";
const PlaylistCard = (props) => {
  const [playlist, setPlaylist] = useState();
  useEffect(() => {
    setPlaylist(() => {
      return props.playlist;
    });
  }, []);
  return (
    <>
      {playlist ? (
        <>
          <Box
            width={"100%"}
            height={"100%"}
            display={"flex"}
            flexDir={"column"}
          >
            <Box
              width={{ base: "90%", md: "200px" }} // Set the size of the square box
              height={{ base: "90%", md: "200px" }}
              flexShrink={0}
              boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
              transition={"200ms"}
              _hover={{
                boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
              }}
            >
              <Image
                src={playlist.cover_image}
                objectFit={"cover"}
                width={"100%"}
                height={"100%"}
              ></Image>
            </Box>
            <Box marginTop={{ base: "1.5%", md: "4%" }}>
              <Text
                fontFamily={"Quicksand"}
                color={"#22092C"}
                fontSize={{ base: "20px", md: "17px" }}
              >
                {playlist.playlist_name}
              </Text>
            </Box>
          </Box>
        </>
      ) : (
        <Text>Uhoh</Text>
      )}
    </>
  );
};

export default PlaylistCard;
