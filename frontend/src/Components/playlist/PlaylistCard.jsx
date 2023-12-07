import React, { useEffect, useState } from "react";
import { Image, Text, Box, VStack } from "@chakra-ui/react";
import { useHistory } from "react-router-dom";
const PlaylistCard = (props) => {
  const [playlist, setPlaylist] = useState();
  const history = useHistory();
  const [stats, setStats] = useState();
  const [profile, setProfile] = useState();
  const [curObsession, setCurObsession] = useState();

  const handlePlaylistClick = () => {
    history.push({
      pathname: "/playlist",
      state: {
        playlist: playlist,
        stats: stats,
        profile: profile,
        curObsession: curObsession,
      },
    });
  };
  useEffect(() => {
    setPlaylist(() => {
      return props.playlist;
    });
    setStats(() => {
      return props.stats;
    });
    setProfile(() => {
      return props.profile;
    });
    setCurObsession(() => {
      return props.curObsession;
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
            alignItems={"center"}
            _hover={{
              textDecoration: "underline",
              cursor: "pointer",
            }}
            onClick={handlePlaylistClick}
          >
            <Box
              width={{ sm: "300px", md: "240px", lg: "180px", xl: "250px" }} // Set the size of the square box
              height={{ sm: "300px", md: "240px", lg: "180px", xl: "250px" }}
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
                alt={`playlist-cover-image for ${playlist.playlist_name}`}
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
