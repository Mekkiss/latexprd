echo "\\section{Spells}"

firstletter="1"
for i in *.tex
do
if [ ${i:0:1} != $firstletter ];
	then
		firstletter=${i:0:1}
		echo "\\subsection{$firstletter}"
	fi
echo "\\input{spells/$i}"
done
