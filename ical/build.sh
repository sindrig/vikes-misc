if [ "$REG_OUT" == "" ]; then
    echo "Missing REG_OUT"
    exit 1
fi
if [ "$VIP_OUT" == "" ]; then
    echo "Missing VIP_OUT"
    exit 1
fi

python create_ical.py 2018.xlsx $REG_OUT --name="Pepsideildin 2018 - Víkingur"
python create_ical.py 2018.xlsx $VIP_OUT --name="Pepsideildin 2018 - Víkingur VIP"\
	--filter_by="self.home=='Víkingur'"\
	--event_edit="self.summary+=' VIP';self.date_end=self.date_start;self.date_start-=datetime.timedelta(hours=1)"
