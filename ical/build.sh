if [ "$REG_OUT" == "" ]; then
    echo "Missing REG_OUT"
    exit 1
fi
if [ "$VIP_OUT" == "" ]; then
    echo "Missing VIP_OUT"
    exit 1
fi
if [ "$KVK_OUT" == "" ]; then
    echo "Missing KVK_OUT"
    exit 1
fi

python create_ical.py 103 $REG_OUT 1.4.2018 30.11.2018 1 --name="Pepsideildin 2018 - Víkingur"
python create_ical.py 103 $VIP_OUT 1.4.2018 30.11.2018 1 --name="Pepsideildin 2018 - Víkingur VIP"\
    --filter_by="self.home=='Víkingur R.'"\
    --event_edit="self.summary+=' VIP';self.date_end=self.date_start;self.date_start-=datetime.timedelta(hours=1)"
python create_ical.py 103 $KVK_OUT 1.4.2018 30.11.2018 0 --name="Pepsideildin 2018 - HK/Víkingur"
