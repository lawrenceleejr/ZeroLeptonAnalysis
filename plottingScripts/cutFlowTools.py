from collections import OrderedDict

def pdgRound(value, error) :
    "Given a value and an error, round and format them according to the PDG rules for significant digits"
    def threeDigits(value) :
        "extract the three most significant digits and return them as an int"
        return int(("%.2e"%float(error)).split('e')[0].replace('.','').replace('+','').replace('-',''))
    def nSignificantDigits(threeDigits) :
        assert threeDigits<1000,"three digits (%d) cannot be larger than 10^3"%threeDigits
        if threeDigits<101 : return 2 # not sure
        elif threeDigits<356 : return 2
        elif threeDigits<950 : return 1
        else : return 2
    def frexp10(value) :
        "convert to mantissa+exp representation (same as frex, but in base 10)"
        valueStr = ("%e"%float(value)).split('e')
        return float(valueStr[0]), int(valueStr[1])
    def nDigitsValue(expVal, expErr, nDigitsErr) :
        "compute the number of digits we want for the value, assuming we keep nDigitsErr for the error"
        return expVal-expErr+nDigitsErr
    def formatValue(value, exponent, nDigits, extraRound=0) :
        "Format the value; extraRound is meant for the special case of threeDigits>950"
        roundAt = nDigits-1-exponent - extraRound
        nDec = roundAt if exponent<nDigits else 0
        return ('%.'+str(nDec)+'f')%round(value,roundAt)
    tD = threeDigits(error)
    nD = nSignificantDigits(tD)
    expVal, expErr = frexp10(value)[1], frexp10(error)[1]
    extraRound = 1 if tD>=950 else 0
    return (formatValue(value, expVal, nDigitsValue(expVal, expErr, nD), extraRound),
            formatValue(error,expErr, nD, extraRound))


def histToCutFlow(hist):

	mybinlabels = []
	cutflow = []
	for ibin in xrange(1,hist.GetNbinsX()+1 ):
		label = hist.GetXaxis().GetBinLabel(ibin).translate(None, " _(),.")
		mybinlabels.append(  label )

		cutflow.append( [label, str(pdgRound( hist.GetBinContent(ibin), 0 )[0]  ) ]  )

	return cutflow


def dictToTable(cutflows,label="SRX"):


	yields=OrderedDict()
	for sample in cutflows:
		yields["Cut"] = zip(*cutflows[sample])[0]
		yields[sample] =  zip(*cutflows[sample])[1]

	# print [sample for sample in yields]
	tableMap = map(list,zip(*[yields[sample] for sample in yields])  )

	outputFile = open("tables/CutFlowTable_%s.tex"%label, 'w')

	outputFile.write(r"""
\begin{table}
\center
\scalebox{0.8}{
\begin{tabular}{r  %s}
\hline
%s
\hline\hline
		"""%(
			" | c "*(len(yields)-1) ,
			" & ".join([sample for sample in yields]) +r"  \\",
			)
		)


	for line in tableMap:
		outputFile.write(  " & ".join(line) +r"   \\")
		outputFile.write( "\n" )


	outputFile.write(r""" 
\hline
\end{tabular}
}
\caption{Cut Flow Table for %s. Event yields per 1 fb$^{-1}$.}
\label{table:table%s}
\end{table}
		"""%(label,label)  )

