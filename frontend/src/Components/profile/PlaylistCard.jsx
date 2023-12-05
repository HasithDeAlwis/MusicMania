import { VStack, Box, Text, Flex, Image } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";

const PlaylistCard = (props) => {
  const [playlists, setPlaylist] = useState();
  const testPlaylist = props.playlists;
  useEffect(() => {
    setPlaylist(() => {
      return props.playlists;
    });
  });
  return (
    <>
      <VStack
        align={"flex-start"}
        margin={2}
        minH={{ base: "100%", md: "30%" }}
      >
        <Box
          bg={"#BE3144"}
          minW={"100%"}
          textAlign={"center"}
          boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
          marginY={2}
          transition={"200ms"}
          _hover={{
            boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
          }}
        >
          <Text
            fontSize={"25px"}
            position="sticky"
            fontFamily="Quicksand"
            margin={"10px"}
            color={"#22092C"}
          >
            My Top Playlist
          </Text>
        </Box>
        <VStack
          overflowY="auto"
          maxH={"200px"}
          justifyItems={"start"}
          align={"flex-start"}
          minW={"100%"}
          minH={"25em"}
          marginTop={0}
          spacing={0}
          boxShadow="4px 4px 0 0 white, 8px 8px 0 0  #BE3144"
        >
          {playlists && (
            <>
              {playlists.map((playlist, id) => (
                <>
                  <Flex
                    key={id}
                    justify={"flex-start"}
                    bg={"#22092C"}
                    transition="transform 0.3s ease-in-out"
                    _hover={{
                      transform: "scale(1.03)",
                    }}
                    minW={"100%"}
                    borderX="3px solid #F05941"
                    borderY="1.5px solid #F05941"
                  >
                    <Box
                      flexBasis={"10%"}
                      minW={"100px"}
                      justifySelf={"start"}
                      display={"block"}
                    >
                      <Image
                        src={playlist.cover_image}
                        objectFit={"cover"}
                      ></Image>
                    </Box>
                    <VStack
                      align={"flex-start"}
                      wordwrap="break-word"
                      textOverflow="ellipsis"
                      maxWidth="100%"
                      justifySelf={"start"}
                    >
                      <Text
                        fontSize={"20px"}
                        margin={1}
                        fontFamily={"Poppins"}
                        color={"#F05941"}
                        overflowWrap={"break-word"}
                        alignItems={"flex-start"}
                      >
                        {playlist.playlist_name}
                      </Text>
                    </VStack>
                  </Flex>
                </>
              ))}
            </>
          )}
        </VStack>
      </VStack>
    </>
  );
};

export default PlaylistCard;
