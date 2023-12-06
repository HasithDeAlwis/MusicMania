import React, { useEffect, useState, useRef } from "react";
import PlaylistCard from "../Components/playlist/PlaylistCard";
import { Wrap, WrapItem, Text, Box, VStack, Flex } from "@chakra-ui/react";
import SpotifyInfoCard from "../Components/profile/SpotifyInfoCard";
const PlaylistPage = (props) => {
  const [allPlaylist, setAllPlaylist] = useState();
  const [stats, setStats] = useState();
  const [profile, setProfile] = useState();
  const [curObsession, setCurObsession] = useState();
  useEffect(() => {
    setAllPlaylist(() => {
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
  });

  return (
    <Box minW={"100%"} display={"flex"} justifyContent={"center"}>
      <Box>
        {stats && profile && curObsession && (
          <SpotifyInfoCard
            stats={stats}
            profile={profile}
            curObsession={curObsession}
          />
        )}
      </Box>

      <Box
        w={"80%"}
        display={"flex"}
        flexWrap={"wrap"}
        justifyContent={"center"}
      >
        <Box
          bg={"#BE3144"}
          minW={"90%"}
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
            My Playlists
          </Text>
        </Box>
        {allPlaylist ? (
          <Flex flexWrap={"wrap"} w={"90%"} justifyContent={"space-around"}>
            {allPlaylist.map((playlist, id) => (
              <>
                <Box
                  flexBasis={{ base: "100%", sm: "75%", md: "25%", lg: "19%" }}
                  flexShrink={0}
                  marginX={"1%"}
                  marginY={"1%"}
                >
                  <PlaylistCard key={id} playlist={playlist} />
                </Box>
              </>
            ))}
          </Flex>
        ) : (
          <Text>Hi</Text>
        )}
      </Box>
    </Box>
  );
};

export default PlaylistPage;
