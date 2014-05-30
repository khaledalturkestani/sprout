import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.PrintWriter;
import java.io.BufferedWriter;
import java.io.FileWriter;


public class CleanUpNetworkTrace {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String carrier = "tmobile";
		String up_or_down = "downlink";
		String input_file = "./cleaned_traces/"+carrier+"-"+up_or_down+".rx";
		//File output_file = new File("~/sprout/att-uplink-mahimahi.rx");
		try {
			PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter("./cleaned_traces/"+carrier+"-"+up_or_down+"-mahimahi.rx")));
			PrintWriter oracular_writer = new PrintWriter(new BufferedWriter(new FileWriter("./cleaned_traces/"+carrier+"-"+up_or_down+"-oracular.rx")));
			BufferedReader br = new BufferedReader(new FileReader(input_file));
			String line = br.readLine();
			long init_time = Long.parseLong(line.substring("recv_time=".length(), line.length()-1));
			//line = br.readLine();
			//System.out.println(init_time);
			//System.out.println(Long.parseLong(line.substring("recv_time=".length(), line.length()-1)));
			writer.println(0);
			//System.out.println(Long.parseLong(line.substring("recv_time=".length(), line.length()-1))-init_time);
			while ((line = br.readLine()) != null) {
				//Scanner in = new Scanner(line).useDelimiter("[^0-9]+");
				//System.out.println(line);
				long time_nano = Long.parseLong(line.substring("recv_time=".length(), line.length()-1))-init_time;
				double time_sec = (double)time_nano/1000000000;
				String oracular_str = up_or_down + " " + time_sec + " delivery 20";
				//long time_millisec = Math.round(time_decimal);
				writer.println(time_sec);
				oracular_writer.println(oracular_str);
			}
			br.close();
			writer.close();
			oracular_writer.close();
		} catch (Exception e) {
			System.out.println(e.toString());
			System.out.println(e.getMessage());
		}
		
	}

}
