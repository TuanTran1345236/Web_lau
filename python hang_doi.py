import heapq
import time

class HangDoiUuTien:
    def __init__(self):
        self.heap = []
        self.w = 0.5

    def them_khach(self, ma_kh, loai_kh, p_base):
        t_den = time.time()
        diem_ban_dau = p_base
        khach_hang = (-diem_ban_dau, t_den, ma_kh, loai_kh, p_base)
        heapq.heappush(self.heap, khach_hang)

    def cap_nhat_diem(self):
        thoi_gian_hien_tai = time.time()
        mang_tam = []

        for diem_am, t_den, ma, loai, p_base in self.heap:
            dt = thoi_gian_hien_tai - t_den
            diem_moi = p_base + (self.w * dt)
            mang_tam.append((-diem_moi, t_den, ma, loai, p_base))

        self.heap = mang_tam
        heapq.heapify(self.heap)

    def goi_khach(self):
        if len(self.heap) == 0:
            print("Hien khong co khach hang nao.")
            return None

        self.cap_nhat_diem()
        khach_uu_tien = heapq.heappop(self.heap)
        diem_am, t_den, ma, loai, p_base = khach_uu_tien
        thoi_gian_cho = time.time() - t_den

        print(f"\n---> QUAY SO 1 XIN MOI KHACH: {ma} ({loai})")
        print(f"     Diem uu tien he thong ghi nhan: {-diem_am:.1f}")
        print(f"     Da cho: {thoi_gian_cho:.1f} giay")

        return ma
import heapq
import time
import csv

class MaxHeapTest:
    def __init__(self):
        self.heap = []

    def them_khach(self, ma_kh, loai_kh, p_base):
        t_den = time.time()
        heapq.heappush(self.heap, (-p_base, t_den, ma_kh, loai_kh, p_base))

class ListTest:
    def __init__(self):
        self.mang = []

    def them_khach(self, ma_kh, loai_kh, p_base):
        t_den = time.time()
        self.mang.append((-p_base, t_den, ma_kh, loai_kh, p_base))
        self.mang.sort()

diem_co_ban = {"Khẩn cấp": 4, "VIP": 3, "Người già": 2, "Người thường": 1, "Thường": 1}

def test_toc_do(ten_file, kieu_chay):
    if kieu_chay == "heap":
        q = MaxHeapTest()
    else:
        q = ListTest()

    dang_cho = set()

    try:
        with open(ten_file, encoding="utf-8-sig") as f:
            lines = list(csv.DictReader(f))
    except:
        return None

    start_time = time.time()

    for dong in lines:
        ma = dong["Mã KH"].strip()
        loai = dong["Loại KH"].strip()
        p_base = diem_co_ban.get(loai, 1)

        if ma not in dang_cho:
            q.them_khach(ma, loai, p_base)
            dang_cho.add(ma)

    return time.time() - start_time

def tinh_trung_binh(ten_file, kieu_chay, so_lan=5):
    tong = 0
    for _ in range(so_lan):
        t = test_toc_do(ten_file, kieu_chay)
        if t is None: return None
        tong += t
    return tong / so_lan

print("-" * 55)
print("Kết quả test tốc độ (chạy trung bình 5 lần)")
print("-" * 55)

for size in [100, 1000, 10000]:
    file_name = f"file {size}.csv"

    t_heap = tinh_trung_binh(file_name, "heap")
    t_list = tinh_trung_binh(file_name, "list")

    if t_heap and t_list:
        print(f"Data {size} dòng -> Heap: {t_heap:.5f}s | List: {t_list:.5f}s")
    else:
        print(f"Lỗi: Không tìm thấy file {file_name}")
import time
import csv

diem_co_ban = {"Khẩn cấp": 4, "VIP": 3, "Người già": 2, "Người thường": 1, "Thường": 1}

def hien_thi_menu():
    print("\n" * 2)
    print("+" + "-"*45 + "+")
    print("|          HỆ THỐNG GỌI SỐ ƯU TIÊN            |")
    print("+" + "-"*45 + "+")
    print("| 1. Bốc số thứ tự mới                        |")
    print("| 2. Gọi khách hàng ưu tiên ra quầy           |")
    print("| 3. Xem danh sách đang xếp hàng              |")
    print("| 4. Nạp dữ liệu mô phỏng từ file CSV         |")
    print("| 0. Thoát hệ thống                           |")
    print("+" + "-"*45 + "+")

def kiem_tra_dau_vao(ma_kh, dang_cho):
    if not ma_kh:
        print("Lỗi: Mã khách hàng không được để trống!")
        return False
    if ma_kh in dang_cho:
        print(f"Lỗi: Mã {ma_kh} đang nằm trong hàng đợi!")
        return False
    return True

def chay_chuong_trinh():
    hd = HangDoiUuTien()
    dang_cho = set()

    while True:
        hien_thi_menu()
        lua_chon = input("Vui lòng chọn chức năng (0-4): ").strip()

        if lua_chon == '1':
            print("\n--- BỐC SỐ MỚI ---")
            ma_kh = input("Nhập Mã Khách Hàng (VD: KH01): ").strip().upper()

            if not kiem_tra_dau_vao(ma_kh, dang_cho):
                time.sleep(2)
                continue

            print("Nhóm khách: 1.Thường | 2.Người già | 3.VIP | 4.Khẩn cấp")
            loai_chon = input("Nhập số (1-4): ").strip()

            map_loai = {'1': 'Người thường', '2': 'Người già', '3': 'VIP', '4': 'Khẩn cấp'}
            loai_kh = map_loai.get(loai_chon, 'Người thường')

            hd.them_khach(ma_kh, loai_kh, diem_co_ban[loai_kh])
            dang_cho.add(ma_kh)
            print(f"Đã đưa {ma_kh} ({loai_kh}) vào hàng đợi.")
            time.sleep(1)

        elif lua_chon == '2':
            print("\n--- GỌI SỐ ---")
            ma_duoc_goi = hd.goi_khach()
            if ma_duoc_goi:
                dang_cho.remove(ma_duoc_goi)
            time.sleep(2)

        elif lua_chon == '3':
            print("\n" + "="*50)
            print("DANH SÁCH KHÁCH HÀNG ĐANG CHỜ".center(50))
            print("="*50)
            if len(hd.heap) == 0:
                print("Hiện tại trống.")
            else:
                hd.cap_nhat_diem()

                danh_sach = sorted(hd.heap)

                print("+" + "-"*12 + "+" + "-"*18 + "+" + "-"*14 + "+")
                print("| Mã KH      | Nhóm Khách       | Tổng Điểm    |")
                print("+" + "-"*12 + "+" + "-"*18 + "+" + "-"*14 + "+")

                for kh in danh_sach:
                    diem_am, t, ma, loai, p = kh
                    print(f"| {ma:<10} | {loai:<16} | {-diem_am:<12.1f} |")

                print("+" + "-"*12 + "+" + "-"*18 + "+" + "-"*14 + "+")

            input("\nNhấn Enter để quay lại menu...")

        elif lua_chon == '4':
            print("\n--- NẠP FILE CSV ---")
            ten_file = input("Nhập tên file (VD: file 100.csv): ").strip()
            try:
                with open(ten_file, encoding="utf-8-sig", newline="") as f:
                    lines = list(csv.DictReader(f))
                count = 0
                for dong in lines:
                    ma = dong["Mã KH"].strip()
                    loai = dong["Loại KH"].strip()
                    if ma and ma not in dang_cho:
                        hd.them_khach(ma, loai, diem_co_ban.get(loai, 1))
                        dang_cho.add(ma)
                        count += 1
                print(f"Đã nạp thành công {count} dòng dữ liệu!")
            except Exception:
                print("Lỗi: Không thể mở file. Vui lòng kiểm tra lại tên file.")
            time.sleep(2)

        elif lua_chon == '0':
            print("\nĐang tắt hệ thống...")
            break

        else:
            print("Chức năng không tồn tại. Vui lòng nhập lại!")
            time.sleep(1)


chay_chuong_trinh()
