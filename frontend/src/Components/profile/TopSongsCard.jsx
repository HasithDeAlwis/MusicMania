import React, { useEffect, useState } from "react";
import { VStack, Box, Text, Flex, Image, Link } from "@chakra-ui/react";
import spotify from "./assets/spotify.svg";

const TopSongsCard = (props) => {
  const [topSongs, setTopSongs] = useState();
  useEffect(() => {
    setTopSongs(() => {
      return props.top_songs;
    });
  });
  return (
    <>
      <VStack
        minH={{ base: "100%", md: "30%" }}
        minW={{ base: "90%", sm: "80%", md: "100%", lg: "100%" }}
        maxW={{ base: "90%", sm: "90%" }}
        marginLeft={{ base: 4, sm: 0 }}
      >
        <Box
          bg={"#BE3144"}
          minW={{ base: "70%", md: "100%" }}
          textAlign={"center"}
          boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
          marginY={2}
          transition={"200ms"}
          _hover={{
            boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
          }}
          alignSelf={"center"}
        >
          <Text
            fontSize={"25px"}
            position="sticky"
            fontFamily="Poppins"
            padding={"10px"}
            color={"#22092C"}
          >
            My Top Songs
          </Text>
        </Box>
        <VStack
          overflowY="auto"
          maxH={"200px"}
          justifyItems={"start"}
          align={"flex-start"}
          minH={"25em"}
          marginTop={0}
          spacing={0}
          boxShadow="4px 4px 0 0 white, 8px 8px 0 0  #BE3144"
          minW={{ base: "100%", sm: "80%", md: "100%" }}
          maxW={{ sm: "90%" }}
          alignSelf={"center"}
        >
          {/*Only display table if recents have been loaded*/}
          {topSongs && (
            <>
              {topSongs.map((song, id) => (
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
                      minW={"80px"}
                      justifySelf={"start"}
                      display={"block"}
                    >
                      <Image src={song.cover_image} objectFit={"cover"}></Image>
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
                        {song.name}
                      </Text>
                      <Flex alignSelf={"start"}>
                        <Text
                          color={"#F05941"}
                          fontSize="18px"
                          fontFamily={"Poppins"}
                          marginLeft={2}
                        >
                          Artist:
                        </Text>
                        {song.artists.map(
                          (artist, index) =>
                            index < 3 && (
                              <Text
                                color="#F05941"
                                fontSize={"14px"}
                                fontFamily="Poppins"
                                marginLeft={1}
                                marginTop={1}
                                border="2px solid #333"
                              >
                                {artist}
                              </Text>
                            )
                        )}
                      </Flex>
                    </VStack>
                    <Link href={song.song_link} ml={"auto"}>
                      <Image
                        marginLeft="auto"
                        src={spotify}
                        justifySelf={"flex-end"}
                        justifyItems={"end"}
                        minW={"45px"}
                        maxW={"45px"}
                      ></Image>
                    </Link>
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

export default TopSongsCard;
