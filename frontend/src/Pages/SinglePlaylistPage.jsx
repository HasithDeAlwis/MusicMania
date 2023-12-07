import { useState, useEffect } from "react";
import React from "react";
import {
  Box,
  Flex,
  Text,
  Image,
  useToast,
  Button,
  VStack,
  position,
} from "@chakra-ui/react";
import PlaylistColumn from "../Components/playlist/PlaylistColumn";
import SpotifyInfoCard from "../Components/profile/SpotifyInfoCard";
const SinglePlaylistPage = (props) => {
  const [playlist, setPlaylist] = useState();
  const [isInitialMount, setIsInitialMount] = useState(true);
  const [stats, setStats] = useState();
  const [profile, setProfile] = useState();
  const [curObsession, setCurObsession] = useState();
  const [playlistSongs, setPlaylistSongs] = useState();
  const [playlsitStats, setPlaylistsStats] = useState();
  const [tracks, setTracks] = useState();
  const toast = useToast();
  useEffect(() => {
    setPlaylist(() => {
      return props.location.state?.playlist;
    });
    setStats(() => {
      return props.location.state?.stats;
    });
    setProfile(() => {
      return props.location.state?.profile;
    });
    setCurObsession(() => {
      return props.location.state?.curObsession;
    });
    console.log(playlist);
  }, []);

  useEffect(() => {
    const getPlaylistInfo = async () => {
      try {
        //Make cal to the spotify api to get the profile
        const playlistResponse = await fetch(
          `/api/spotify/get-playlist-info/${playlist.id}`,
          {
            headers: new Headers({ "content-type": "application/json" }),
            method: "POST",
          }
        );

        const playlistData = await playlistResponse.json();

        const data = await playlistData;
        console.log(data);
        setPlaylistSongs(() => {
          return data["song-data"];
        });
        setPlaylistsStats(() => {
          return data["stats"];
        });
        setTracks(() => {
          return data["total-tracks"];
        });
        if (!playlistResponse.ok) {
          throw new Error(`${playlistData.error}`);
        }
        return data;
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
    if (!isInitialMount) {
      getPlaylistInfo();
    } else {
      setIsInitialMount(false);
    }
  }, [playlist]);
  return (
    <>
      {playlist && playlistSongs && playlsitStats && tracks && (
        <>
          <Box bgImage={playlist.cover_image} w={"100%"} filter="blur(0px)">
            <Flex
              flexDir={{ base: "column", md: "row" }}
              align="center"
              justify="center"
              h="100%"
              w="100%"
              backdropFilter="blur(20px) brightness(70%)" // Adjust the blur intensity for the foreground
              padding={4}
            >
              <Box
                flexShrink={0}
                display="flex"
                width={{ sm: "300px", md: "400px", lg: "450px", xl: "470px" }} // Set the size of the square box
                height={{ sm: "300px", md: "400px", lg: "450px", xl: "470px" }}
              >
                <Image
                  padding={"5%"}
                  objectFit="contain"
                  src={playlist.cover_image}
                  alt={`Playlist cover for ${playlist.playlist_name}`}
                ></Image>
              </Box>
              <Box>
                <Text
                  fontSize={"22px"}
                  fontWeight={999}
                  fontFamily={"Poppins"}
                  color={"white"}
                >
                  {playlist.playlist_name}
                </Text>
                <Box>
                  <VStack
                    bg={"white"}
                    borderRadius={"xl"}
                    marginTop={1}
                    padding={2}
                    transition={"200ms"}
                    boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  white"
                    _hover={{
                      boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  white",
                    }}
                  >
                    <Text
                      fontFamily={"Poppins"}
                      fontSize={"22px"}
                      fontWeight={900}
                      color={"#22092C"}
                    >
                      Playlist Info
                    </Text>
                    <Box textAlign={"center"}>
                      <Text>Length: {tracks} tracks</Text>
                      <Text fontFamily={"Poppins"}>
                        Danceability: {playlsitStats[2].toFixed(0)}
                      </Text>
                      <Text fontFamily={"Poppins"}>
                        Happiness: {(playlsitStats[0] * 100).toFixed(0)}
                      </Text>
                      <Text fontFamily={"Poppins"}>
                        Energy: {(playlsitStats[1] * 100).toFixed(0)}
                      </Text>
                    </Box>
                  </VStack>
                  <Button
                    fontFamily={"Poppins"}
                    color={"#22092C"}
                    bgColor={"white"}
                    w={"100%"}
                    marginTop={4}
                    borderRadius={"xl"}
                    transition={"200ms"}
                    boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  white"
                    _hover={{
                      boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  white",
                    }}
                  >
                    Add Playlist
                  </Button>
                </Box>
              </Box>
            </Flex>
          </Box>
          <Box
            w="100%"
            display={"flex"}
            justifyContent={"center"}
            flexWrap={"wrap"}
            flexDir={{ base: "column", md: "row" }}
          >
            <Box
              bg={"#BE3144"}
              minW={"81%"}
              maxW={"90%"}
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
                fontFamily="Quicksand"
                margin={"10px"}
                color={"#22092C"}
              >
                Playlist Songs
              </Text>
            </Box>
            <Box
              flexShrink={0}
              flexBasis={{ base: "70%", sm: "70%", md: "40%", lg: "25%" }}
              display="flex"
              flexDir={"column"}
              alignItems={"center"}
              alignSelf={{ md: "flex-start" }}
              position={{ md: "sticky" }}
              top={"13%"}
            >
              {stats && profile && curObsession && (
                <SpotifyInfoCard
                  stats={stats}
                  profile={profile}
                  curObsession={curObsession}
                />
              )}
            </Box>
            <Flex
              alignSelf="center"
              w={{ base: "95%", md: "60%" }}
              flexDir={"column"}
            >
              {playlistSongs ? (
                playlistSongs.map((song, index) => (
                  <Box key={index} margin={1}>
                    <PlaylistColumn song={song} />
                  </Box>
                ))
              ) : (
                <Text>RuhRoh</Text>
              )}
            </Flex>
          </Box>
        </>
      )}
    </>
  );
};

export default SinglePlaylistPage;
