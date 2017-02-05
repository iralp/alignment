import alignment.metrics.*;
import alignment.metrics.SemanticSimilarity.SimilarityMeasure;
import alignment.util.*;

import java.util.*;
import java.io.*;

public class GetScores {
	
	public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException {
		if (args.length != 3)	{
			System.out.println("Invalid input! Programing exiting...");
		} else {
			printScores(args[0], args[1], args[2]);
		}
	}
	
	public static void printScores(String file1Path, String file2Path, String outFilePath) throws FileNotFoundException, UnsupportedEncodingException {
		//boolean indicates that the metric will use the structural semantic similarity measure
		ComparisonMetric metric = new SumMaxIdf(SimilarityMeasure.WORDNET, Utilities.loadLemmaIdfScores(), true);
		
		//loads sentences from the source files into the triples form
		List<List<String[]>> file1Triples = Utilities.fileToTriples(new File(file1Path), Utilities.loadLemmaMappings());
		List<List<String[]>> file2Triples = Utilities.fileToTriples(new File(file2Path), Utilities.loadLemmaMappings());
		
		//opens a PrintStream to write to the output file
		PrintStream output = new PrintStream(new File(outFilePath), "UTF-8");
		
		double[][] scores = new double[file1Triples.size()][file2Triples.size()];
		
		//computes scores for all sentence pairs and stores the output in the matrix
		for (int i = 0; i < file1Triples.size(); i++)	{
			for (int j = 0; j < file2Triples.size(); j++)	{
				scores[i][j] = metric.compare(file1Triples.get(i), file2Triples.get(j));
			}
		}
		
		//writes matrix to output in tab-delimited form
		//columns correspond to sentences in file2 and rows correspond to the sentences in file1
		for (int i = 0; i < file1Triples.size(); i++)	{
			String row = "" + scores[i][0];
			
			for (int j = 1; j < file2Triples.size(); j++)	{
				row += "\t" + scores[i][j];
			}
			output.print(row + "\n");
		}
		output.close();
	}

}
