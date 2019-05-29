fun blah([], headofAlph : char) = false
| blah(head_string::tail_string, headofAlph) =
	if headofAlph = head_string
	then true
	else blah(tail_string, headofAlph)
	
exception Empty

fun trueOrFalse(head_string::tail_string, []) = "true\n"
| trueOrFalse ([], []) = raise Empty
| trueOrFalse ([], head_string::tail_string) = raise Empty
| trueOrFalse(head_string::tail_string, headofAlph::tailofAlph) =	
	if blah(head_string::tail_string, headofAlph)
	then trueOrFalse(head_string::tail_string, tailofAlph)
	else "false\n"

fun pangram(inputFile : string, outputFile : string) =
	let
		val ins = TextIO.openIn inputFile
		val outs = TextIO.openOut outputFile
		val readSentence = TextIO.inputLine ins
		val alpha = "abcdefghijklmnopqrstuvwxyz"


		fun helper (readSentence : string option) =
			case readSentence of
			  NONE => (TextIO.closeIn ins; TextIO.closeOut outs)
			| SOME(c) => (TextIO.output(outs,trueOrFalse(explode(c),explode(alpha)));
			helper(TextIO.inputLine ins))
	in
		helper(readSentence)
	end;