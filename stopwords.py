from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def indonesia():
    stop_factory = StopWordRemoverFactory()
    nama_hari = ['senin','selasa','rabu','kamis','jumat','sabtu','minggu']
    nama_bulan = [
        'januari','februari','maret','april',
        'mei','juni','juli','agustus',
        'september','oktober','november','desember'
    ]

    more_stopword = [
        'jadi','ujar','baik','umum','dekat',
        'pergi','sibuk','tahun','tingkat','sebutkan',
        'jumlah','kata','harga','besar','kecil',
        'dukung','main','lebih', 'baru','garagara',
        'tersebut',"tak","sangat","lebih","langkah",
        "negara", 'tetap', 'bersama', 'mencapai'
    ]

    verbs = [
        # Kata kerja bantu / penghubung
        "adalah", "menjadi", "merupakan", "ialah", "yaitu", "yakni",

        # Kata kerja pelaporan
        "mengatakan", "menyatakan", "menjelaskan", "menuturkan", 
        "mengungkapkan", "melaporkan", "menambahkan", "menyebutkan", 
        "mengakui"

        # Kata kerja umum / generik
        "melakukan", "membuat", "menggunakan", "memiliki", 
        "terdapat", "terjadi", "dilakukan", "diberikan", 
        "dimiliki", "didapatkan"
    ]

    temporal_words = [
        # Kata keterangan waktu / urutan kejadian
        "kemudian", "setelah", "sebelum", "selanjutnya", "lalu", 
        "berikutnya", "hingga", "sampai", "sejak", "ketika", 
        "tatkala", "pada akhirnya", "pada saat itu", "waktu itu",
        "sementara", "seraya", "seketika", "sesudah", "barulah", "kini"
    ]

    quantity_words = [
        # Kata kuantitas atau jumlah tidak pasti
        "sedikit", "banyak", "beberapa", "sebagian", "jumlah", 
        "berjumlah", "tak sedikit", "lumayan", 
        "cukup", "sangat banyak", "lebih sedikit", "berlimpah", 
        "segelintir", "sejumlah", "terhitung", "terbatas","dibandingkan"
    ]

    uncertainty_words = [
        # Kata yang menyatakan kemungkinan atau ketidakpastian
        "kemungkinan", "mungkin", "barangkali", "agaknya", 
        "sepertinya", "kiranya", "diperkirakan", "langsung",
        "diramalkan", "diduga", "dikhawatirkan", "tidak pasti",
        "entah", "andaikan", "sekiranya", "jika", "apabila",
        "barangkali", "sedikit kemungkinan",'dipastikan'
    ]

    
    list_stop_word = stop_factory.get_stop_words() \
                        + nama_hari \
                        + nama_bulan \
                        + verbs \
                        + uncertainty_words \
                        + temporal_words \
                        + quantity_words \
                        + more_stopword
    
    return set(list_stop_word)

def english():
    stop_words = set(stopwords.words('english'))
    return stop_words