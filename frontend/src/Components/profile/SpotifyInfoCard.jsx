import { Box, VStack, Text, Image, Flex } from "@chakra-ui/react";
import React from "react";

const SpotifyInfoCard = (props) => {
  const stats = props.stats;
  const profile = props.profile;
  console.log(stats);
  const artistBanner = props.artistBanner;
  const curObsession = props.curObsession;
  const valence = stats[0];
  const energy = stats[1];
  const danceability = stats[2];
  const popularity = stats[3];
  let popularityDiss = "";
  let happinessDiss = "";

  //Determining what quote to use based on the stats of the spotify user

  //get the quote for valence
  if (valence > 80) {
    happinessDiss = "Fortunately, I am the happiest I have ever been 😺!";
  } else if (valence > 60) {
    happinessDiss = "Good thing I've been happy recently 😺!";
  } else if (valence > 40) {
    happinessDiss = "Yea... its rought right now 😭";
  } else {
    happinessDiss = "Fortunately, I'm happy! Just kidding!!! I'm depressed 💀";
  }

  //get the quote for popularity
  if (popularity > 75) {
    popularityDiss = "Super basic 🥱";
  } else if (popularity > 50) {
    popularityDiss = "Only kind of basic 😐";
  } else if (popularity > 40) {
    popularityDiss = "More basic than I think it is... 🫣";
  } else {
    popularityDiss = "Soooo obscure, im so cool and quirky 🥰";
  }

  //set all artists
  let allArtists = "";
  console.log(curObsession);
  //get the artists of the current obsession
  const hello = curObsession.artists.map((artist, index) => {
    if (index != 0) {
      allArtists += ", " + artist;
    } else {
      allArtists = artist;
    }
  });
  return (
    <>
      <Box
        margin={5}
        boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
        transition={"200ms"}
        _hover={{
          boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
        }}
      >
        <VStack bg={"#BE3144"} padding={2} textAlign={"center"}>
          <Text
            color={"#22092C"}
            fontFamily={"Quicksand"}
            borderBottom={"2px solid #FFF"}
          >
            {profile.spotifyUserName}
          </Text>
          <Flex>
            <Image
              width="100%"
              src={profile.profilePicture}
              objectFit={"cover"}
            />
          </Flex>

          <Text
            color={"#22092C"}
            fontFamily={"Quicksand"}
            borderBottom={"2px solid #FFF"}
          >
            Happiness Score: {(valence * 100).toFixed(0)}
          </Text>

          <Text
            color={"#22092C"}
            fontFamily={"Quicksand"}
            borderBottom={"2px solid #FFF"}
          >
            Basic Score: {popularity.toFixed(0)}
          </Text>
          <Text
            color={"#22092C"}
            fontFamily={"Quicksand"}
            borderBottom={"2px solid #FFF"}
          >
            Energy Score: {energy.toFixed(0)}
          </Text>
          <Text
            color={"#22092C"}
            fontFamily={"Quicksand"}
            borderBottom={"2px solid #FFF"}
          >
            Danceability Score: {danceability.toFixed(0)}
          </Text>

          <Text
            color={"#22092C"}
            fontFamily={"Quicksand"}
            borderBottom={"2px solid #FFF"}
          >
            Current Obsession: {curObsession.song_name} by {allArtists}
          </Text>
        </VStack>
      </Box>
    </>
  );
};

export default SpotifyInfoCard;
