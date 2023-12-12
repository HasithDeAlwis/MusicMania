import React from "react";
import { useEffect, useState, useRef } from "react";
import { useToast, Box, Flex, Button, VStack } from "@chakra-ui/react";
import TopArtistsCard from "../Components/profile/TopArtistsCard";
import SpotifyInfoCard from "../Components/profile/SpotifyInfoCard";
import GenresCard from "../Components/profile/GenresCard";
import RecentlyPlayedCard from "../Components/profile/RecentlyPlayedCard";
import TopSongsCard from "../Components/profile/TopSongsCard";
import { useHistory } from "react-router-dom";
import { useLocation } from "react-router-dom";

const ProfilePage = (props) => {
  const [curObsession, setCurObsession] = useState();
  const [songs, setSongs] = useState();
  const [artists, setArtists] = useState();
  const [recents, setRecents] = useState();
  const [stats, setStats] = useState();
  const [playlist, setPlaylist] = useState();
  const [profile, setProfile] = useState();
  const [topGenres, setTopGenres] = useState();
  const toast = useToast();
  const [isInitialMount, setIsInitialMount] = useState(true);
  const location = useLocation();
  const history = useHistory();

  const queryParameters = new URLSearchParams(location.search);
  const token = queryParameters.get("user");

  useEffect(() => {
    const getProfileInfo = async () => {
      try {
        //Make cal to the spotify api to get the profile
        const profileResponse = await fetch("/api/spotify/get-profile", {
          headers: new Headers({ "content-type": "application/json" }),
          method: "POST",
        });

        const profileData = await profileResponse.json();

        const data = await profileData;
        if (!profileResponse.ok) {
          throw new Error(`${profileData.error}`);
        }
        setProfile(data[0]);

        return profileData;
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
    const getTopSongs = async () => {
      try {
        //Make call to get the spotify api to get the users top songs
        const topSongsResponse = await fetch("/api/spotify/top-songs", {
          headers: new Headers({ "content-type": "application/json" }),
          method: "POST",
        });

        const topSongsData = await topSongsResponse.json();
        const data = await topSongsData;

        if (!topSongsResponse.ok) {
          throw new Error(`${topSongsData.error}`);
        }

        setSongs(data);
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
    const getRecentlyPlayed = async () => {
      try {
        //Make call to get the spotify api to get the users recent songs songs
        const recentSongsResponse = await fetch(
          "/api/spotify/recently-played",
          {
            headers: new Headers({ "content-type": "application/json" }),
            method: "POST",
          }
        );
        //save data
        let recentSongsData = await recentSongsResponse.json();
        recentSongsData = await recentSongsData;
        //check for error
        if (!recentSongsResponse.ok) {
          throw new Error(`${recentSongsData.error}`);
        }
        //set data accordingly
        setRecents(() => {
          return recentSongsData.recents;
        });
        setStats(() => {
          return recentSongsData.analysis;
        });
      } catch (error) {
        //toast the error
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

    const getTopArtists = async () => {
      try {
        //Make call to get the spotify api to get the users top songs
        const topArtistsResponse = await fetch("/api/spotify/top-artists", {
          headers: new Headers({ "content-type": "application/json" }),
          method: "POST",
        });

        const topArtistsData = await topArtistsResponse.json();
        const data = await topArtistsData;
        if (!topArtistsResponse.ok) {
          throw new Error(`${topArtistsData.error}`);
        }

        setArtists(() => {
          return data["artist"];
        });
        setTopGenres(() => {
          return data["top-genres"];
        });
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

    const getPlaylist = async () => {
      try {
        //Make call to get the spotify api to get the users top songs
        const allPlaylistResponse = await fetch("/api/spotify/playlist", {
          headers: new Headers({ "content-type": "application/json" }),
          method: "POST",
        });

        const allPlaylsitData = await allPlaylistResponse.json();
        const data = await allPlaylsitData;
        if (!allPlaylistResponse.ok) {
          throw new Error(`${allPlaylsitData.error}`);
        }

        setPlaylist(() => {
          return data;
        });
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

    const fetchData = async () => {
      await getTopSongs();
      await getProfileInfo();
      await getRecentlyPlayed();
      await getTopArtists();
      await getPlaylist();
    };

    const accessDataBase = async (token) => {
      try {
        //Make call to get the spotify api to get the users top songs
        const allInfoResponse = await fetch(
          `/api/spotify/get-user-spotify-info?token=${token}`,
          {
            headers: new Headers({ "content-type": "application/json" }),
            method: "GET",
          }
        );

        const allInfoData = await allInfoResponse.json();
        const data = await allInfoData;

        if (!allInfoResponse.ok) {
          throw new Error(`${allInfoData.error}`);
        }
        //set the songs
        setSongs(() => {
          return data["top-songs"];
        });
        //set hte playlists
        setPlaylist(() => {
          return data["playlist"];
        });
        //set the recents
        setRecents(() => {
          return data["recent-songs"];
        });
        //set the stats
        setStats(() => {
          return data["stats"];
        });
        //set the profile
        setProfile(() => {
          return data["profile"][0];
        });

        setTopGenres(() => {
          return data["top-genres"];
        });
        setArtists(() => {
          return data["top-artists"];
        });
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
    const fetchOtherUserData = async (token) => {
      await accessDataBase(token);
    };

    if (token) {
      fetchOtherUserData(token);
    } else {
      fetchData();
    }
  }, []);

  useEffect(() => {
    const addToDB = async (
      songs,
      artists,
      recentSongs,
      recentStats,
      profile,
      playlist
    ) => {
      try {
        //Make call to get the spotify api to get the users top songs
        const dbResponse = await fetch("/api/spotify/update-user-info", {
          headers: new Headers({ "content-type": "application/json" }),
          method: "POST",
          body: JSON.stringify({
            "recent-songs": recentSongs,
            "user-profile": profile,
            "top-songs": songs,
            "top-artists": artists,
            "user-stats": recentStats,
            "user-playlist": playlist,
          }),
        });
        const dbData = await dbResponse.json();
        if (!dbResponse.ok) {
          throw new Error(`${dbData.error}`);
        }
      } catch (error) {
        toast({
          title: "Erro Occured!!",
          status: "error",
          description: error.message,
          duration: 5000,
          isClosable: true,
          position: "bottom",
        });
      }
    };
    const getCurrentObsesion = (recentSongs) => {
      let maxCount = 0;
      let count = 0;
      let maxIndex = 0;
      recentSongs.map((song, index) => {
        count = 0;
        recentSongs.map((curSong, index2) => {
          if (song.song_name === curSong.song_name) {
            count += 1;
          }
        });
        if (count > maxCount) {
          maxCount = count;
          maxIndex = index;
        }
      });
      return recentSongs[maxIndex];
    };
    //chcek to see if we're in our first mount, if we are then don't run this useEffect()
    if (isInitialMount) {
      setIsInitialMount(() => {
        return false;
      });
    } else {
      //get the current obsession
      setCurObsession(() => {
        return getCurrentObsesion(recents);
      });
      if (!token) {
        //update the database
        addToDB(songs, artists, recents, stats, profile, playlist);
      }
    }
  }, [playlist]);

  return (
    <>
      <Flex minW={"100%"} flexDir={{ base: "column", md: "row" }}>
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
            <>
              <SpotifyInfoCard
                stats={stats}
                profile={profile}
                curObsession={curObsession}
              />
            </>
          )}
          {profile && stats && curObsession && (
            <Box>
              <Button
                bg="#22092C"
                textColor={"#BE3144"}
                minW={"50%"}
                flexBasis={"5%"}
                _hover={{ bg: "#49095C", textColor: "#BE3144" }}
                onClick={() =>
                  history.push({
                    pathname: "/user-playlist",
                    state: {
                      playlist: playlist,
                      stats: stats,
                      profile: profile,
                      curObsession: curObsession,
                    },
                  })
                }
              >
                View Playlist
              </Button>
            </Box>
          )}
        </Box>

        <Flex
          justify={{ base: "center", md: "space-around" }}
          alignItems={{ base: "start", md: "" }}
          flexDir={{ base: "column", md: "row" }}
          wrap={"wrap"}
        >
          <Box flexBasis={"40%"} flexShrink={1}>
            {artists && <TopArtistsCard artists={artists} />}
          </Box>
          <Box flexBasis={"40%"} flexShrink={1}>
            {topGenres && <GenresCard genres={topGenres} />}
          </Box>
          <Box flexBasis={"40%"} flexShrink={1}>
            {recents && (
              <RecentlyPlayedCard recents={recents} display={"flex"} />
            )}
          </Box>
          <Box flexBasis={"40%"} flexShrink={1}>
            {songs && <TopSongsCard top_songs={songs} />}
          </Box>
        </Flex>
      </Flex>
    </>
  );
};

export default ProfilePage;
