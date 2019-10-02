import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;

public class CSV {
	
    public static String[][] getCSVData(String csvFile, int i, int j) {
		
		BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";
        String[] position = null;
        String person[][] = new String[i][j];

        try {

            br = new BufferedReader(new FileReader(csvFile));
            int p = 0;
            while ((line = br.readLine()) != null) {
            	
                position = line.split(cvsSplitBy);
                person[p][0]=position[1];
                person[p][1]=position[5];
                person[p][2]=position[4];
  
                p++; 
            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        return person;
    }

}