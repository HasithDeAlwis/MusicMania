import React from "react";
import { Box, Text, VStack, Flex, Image, Link } from "@chakra-ui/react";
import spotify from "./assets/spotify.svg";
const TopArtistsCard = (props) => {
  const artists = props.artists;
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
            My Top Artists
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
          {artists.map((artist, index) => (
            <Flex
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
                <Image src={artist.images} objectFit={"cover"}></Image>
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
                  {artist.name}
                </Text>
                <Flex alignSelf={"start"}>
                  <Text
                    color={"#F05941"}
                    fontSize="18px"
                    fontFamily={"Poppins"}
                    marginLeft={2}
                  >
                    Genres:
                  </Text>
                  {artist.genres.map(
                    (genre, index) =>
                      index < 3 && (
                        <Text
                          color="#F05941"
                          fontSize={"14px"}
                          fontFamily="Poppins"
                          marginLeft={1}
                          marginTop={1}
                          border="2px solid #333"
                        >
                          {genre}
                        </Text>
                      )
                  )}
                </Flex>
              </VStack>
              <Link href={artist.artists_link} ml={"auto"}>
                <Image
                  marginLeft="auto"
                  src={spotify}
                  justifySelf={"flex-end"}
                  justifyItems={"end"}
                  minW={"50px"}
                ></Image>
              </Link>
            </Flex>
          ))}
        </VStack>
      </VStack>
    </>
  );
};

export default TopArtistsCard;
