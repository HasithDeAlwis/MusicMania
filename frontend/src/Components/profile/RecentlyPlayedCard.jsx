import React from "react";
import { VStack, Box, Text, Flex, Image, Link } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import spotify from "./assets/spotify.svg";
const RecentlyPlayedCard = (props) => {
  const [recents, setRecents] = useState();
  useEffect(() => {
    setRecents(() => {
      return props.recents;
    });
  });
  return (
    <>
      <VStack
        minH={{ base: "100%", md: "30%" }}
        minW={{ base: "90%", sm: "80%", md: "100%", lg: "100%" }}
        maxW={{ base: "90%", sm: "90%" }}
        marginLeft={{ base: 4, sm: "0" }}
        alignItems={"center"}
        marginBottom={2}
      >
        <Box
          bg={"#BE3144"}
          textAlign={"center"}
          boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
          marginY={2}
          transition={"200ms"}
          _hover={{
            boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
          }}
          minW={{ base: "70%", md: "100%" }}
          alignSelf={"center"}
        >
          <Text
            fontSize={"25px"}
            fontFamily="Quicksand"
            margin={"10px"}
            color={"#22092C"}
          >
            My Recently Played
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
          {recents && (
            <>
              {recents.map((recent, id) => (
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
                      <Image
                        src={recent.cover_images}
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
                        {recent.song_name}
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
                        {recent.artists.map(
                          (artist, index) =>
                            index < 3 && (
                              <Text
                                color="#F05941"
                                fontSize={"14px"}
                                fontFamily="Poppins"
                                marginLeft={1}
                                marginTop={1}
                              >
                                {artist}
                              </Text>
                            )
                        )}
                      </Flex>
                    </VStack>
                    <Link href={recent.song_link} ml={"auto"}>
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

export default RecentlyPlayedCard;
