import React from "react";
import { useEffect, useState, useRef } from "react";
import { useToast, Box, Flex } from "@chakra-ui/react";
import TopArtistsCard from "../Components/profile/TopArtistsCard";
import SpotifyInfoCard from "../Components/profile/SpotifyInfoCard";
const ProfilePage = () => {
  const [curObsession, setCurObsession] = useState();
  const [songs, setSongs] = useState();
  const [artists, setArtists] = useState();
  const [recents, setRecents] = useState();
  const [stats, setStats] = useState();
  const [playlist, setPlaylist] = useState();
  const [profile, setProfile] = useState();
  const toast = useToast();
  const [isInitialMount, setIsInitialMount] = useState(true);

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
        console.log("profile", data[0]);
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
        //Make call to get the spotify api to get the users top songs
        const recentSongsResponse = await fetch(
          "/api/spotify/recently-played",
          {
            headers: new Headers({ "content-type": "application/json" }),
            method: "POST",
          }
        );

        let recentSongsData = await recentSongsResponse.json();
        recentSongsData = await recentSongsData;
        if (!recentSongsResponse.ok) {
          throw new Error(`${recentSongsData.error}`);
        }

        setRecents(recentSongsData.recents);
        setStats(recentSongsData.analysis);
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
      await getPlaylist();
      await getTopArtists();
    };
    fetchData();
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
      console.log(recentSongs);
      recentSongs.map((song, index) => {
        recentSongs.map((curSong, index2) => {
          if (curSong == song) {
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
    if (isInitialMount) {
      setIsInitialMount(() => {
        return false;
      });
    } else {
      setCurObsession(() => {
        return getCurrentObsesion(recents);
      });
      addToDB(songs, artists, recents, stats, profile, playlist);
    }
  }, [artists]);
  return (
    <>
      <Flex
        minW={"100%"}
        flexDir={{ base: "column", md: "row" }}
        alignItems={{ base: "center" }}
      >
        <Box
          flexShrink={0}
          flexBasis={{ base: "70%", sm: "70%", md: "40%", lg: "25%" }}
        >
          {stats && profile && curObsession && (
            <SpotifyInfoCard
              stats={stats}
              profile={profile}
              curObsession={curObsession}
              artistBanner={artists[4].images}
            />
          )}
        </Box>
        <Flex
          justify={"space-around"}
          flexBasis={"auto"}
          flexDir={{ base: "column", md: "row" }}
        >
          <Box flexBasis={"40%"}>
            {artists && <TopArtistsCard artists={artists} />}
          </Box>
          <Box></Box>
        </Flex>
      </Flex>
    </>
  );
};

export default ProfilePage;
