import React, { useState } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "react-chartjs-2";
import { useEffect } from "react";
import { VStack, Box, Text } from "@chakra-ui/react";
ChartJS.register(ArcElement, Tooltip, Legend);

const GenresCard = (props) => {
  const [chartData, setChartData] = useState();
  const [chartSettings, setChartSettings] = useState();
  useEffect(() => {
    const countFrequency = (genres) => {
      //define a frequency dictionary
      const genreFrquency = {};
      //for every element of the array
      for (const genre of genres) {
        //increase the frequency of that item by 1
        genreFrquency[genre] = (genreFrquency[genre] || 0) + 1;
      }
      return genreFrquency;
    };
    //function that sorts the dictionary into a list by frequency
    const sortByFrequency = (genres) => {
      const genreFrequency = countFrequency(genres);
      const sortedGenres = Object.keys(genreFrequency).sort(
        (a, b) => genreFrequency[b] - genreFrequency[a]
      );
      // Take the top 15 genres only
      const top10Genres = sortedGenres.slice(0, 15);
      // Create a dictionary for the top 15 genres with their frequencies
      const top10GenreFrequency = {};
      //go through every genre in the top 10 genres and assign them a frequency based on their frequency found at the start
      for (const genre of top10Genres) {
        //assign the frequency to the new dict
        top10GenreFrequency[genre] = genreFrequency[genre];
      }
      return top10GenreFrequency;
    };

    const genres = props.genres;
    const topGenres = sortByFrequency([...genres]);
    const pieChartData = {
      labels: Object.keys(topGenres).map((genre) => genre),
      datasets: [
        {
          label: "Top Genres",
          data: Object.values(topGenres).map((frequency) => frequency),
          borderWidth: 1,
          backgroundColor: [
            "#FF5733", // Vivid Orange
            "#FFC300", // Vivid Yellow
            "#4CAF50", // Green
            "#00BCD4", // Cyan
            "#2196F3", // Blue
            "#9C27B0", // Purple
            "#FF4081", // Pink
            "#FF5252", // Red
            "#FFD700", // Gold
            "#FF6347", // Tomato
            "#00FF00", // Lime
            "#00FFFF", // Aqua
            "#1E90FF", // Dodger Blue
            "#8A2BE2", // Blue Violet
            "#FF69B4", // Hot Pink
          ],
        },
      ],
    };
    const options = {
      plugins: {
        legend: {
          display: true,
          labels: {
            color: "#BE3144", // Change label color
            font: {
              size: 12, // Change label font size
              weight: "bold", // Change label font weight
              family: "Poppins",
            },
          },
        },
      },
    };
    setChartData(() => {
      return pieChartData;
    });
    setChartSettings(() => {
      return options;
    });
  }, []);

  return (
    <>
      <VStack
        alignItems={"center"}
        margin={2}
        minW={{ base: "90%", sm: "90%", md: "90%", lg: "100%" }}
        maxW={{ base: "95%", sm: "100%" }}
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
          alignSelf={"center"}
          minW={{ base: "70%", md: "100%" }}
        >
          <Text
            fontSize={"25px"}
            position="sticky"
            fontFamily="Poppins"
            padding={"10px"}
            color={"#22092C"}
          >
            My Top Genres
          </Text>
        </Box>
        <Box
          bg={"#22092C"}
          textAlign={"center"}
          boxShadow="4px 4px 0 0 white, 8px 8px 0 0  #BE3144"
          transition={"200ms"}
          _hover={{
            boxShadow: "6px 6px 0 0 white, 10px 10px 0 0  #BE3144",
          }}
          minW={{ base: "90%" }}
          padding={"2px"}
          alignSelf={"center"}
          display={"flex"}
          minH={"25em"}
          justifyContent={"center"}
        >
          {chartData && chartSettings && (
            <Pie data={chartData} options={chartSettings} />
          )}
        </Box>
      </VStack>
    </>
  );
};

export default GenresCard;
