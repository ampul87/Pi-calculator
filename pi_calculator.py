#!/usr/bin/env python3
import requests
from typing import Optional

class PiCalculator:
    """Kalkulator untuk penukaran Pi Network (PI) ke USD dan MYR menggunakan API masa nyata."""

    def __init__(self):
        self.pi_price_usd = None
        self.usd_to_myr = None
        self.api_urls = {
            "pi_price": "https://api.coingecko.com/api/v3/simple/price?ids=pi-network&vs_currencies=usd",
            "usd_to_myr": "https://api.exchangerate.host/convert?from=USD&to=MYR"
        }

    def get_pi_price_usd(self) -> Optional[float]:
        """Mendapatkan harga Pi Network (PI) dalam USD dari CoinGecko API."""
        try:
            response = requests.get(self.api_urls["pi_price"], timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["pi-network"]["usd"]
        except (requests.RequestException, KeyError) as e:
            print(f"Ralat mendapatkan harga PI: {e}")
            return None

    def get_usd_to_myr(self) -> Optional[float]:
        """Mendapatkan kadar tukaran USD ke MYR dari exchangerate.host API."""
        try:
            response = requests.get(self.api_urls["usd_to_myr"], timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["result"]
        except (requests.RequestException, KeyError) as e:
            print(f"Ralat mendapatkan kadar USD ke MYR: {e}")
            return None

    def pi_to_usd(self, pi_amount: float) -> Optional[float]:
        """Mengira nilai PI dalam USD."""
        return pi_amount * self.pi_price_usd if self.pi_price_usd else None

    def pi_to_myr(self, pi_amount: float) -> Optional[float]:
        """Mengira nilai PI dalam MYR."""
        usd_value = self.pi_to_usd(pi_amount)
        return usd_value * self.usd_to_myr if usd_value and self.usd_to_myr else None

    def usd_to_pi(self, usd_amount: float) -> Optional[float]:
        """Mengira jumlah PI daripada USD."""
        return usd_amount / self.pi_price_usd if self.pi_price_usd else None

    def myr_to_pi(self, myr_amount: float) -> Optional[float]:
        """Mengira jumlah PI daripada MYR."""
        usd_value = myr_amount / self.usd_to_myr if self.usd_to_myr else None
        return self.usd_to_pi(usd_value) if usd_value and self.pi_price_usd else None

    def run(self):
        """Menjalankan kalkulator interaktif."""
        print("Kalkulator Penukaran Pi Network (PI) ke USD dan MYR (Masa Nyata)")
        
        # Dapatkan harga terkini
        self.pi_price_usd = self.get_pi_price_usd()
        self.usd_to_myr = self.get_usd_to_myr()
        
        if self.pi_price_usd is None or self.usd_to_myr is None:
            print("Gagal mendapatkan data harga terkini. Sila cuba lagi kemudian.")
            return
        
        print(f"Kadar semasa: 1 PI = ${self.pi_price_usd:.4f} USD, 1 USD = RM{self.usd_to_myr:.2f} MYR")
        
        while True:
            print("\nPilih jenis penukaran:")
            print("1. PI ke USD")
            print("2. PI ke MYR")
            print("3. USD ke PI")
            print("4. MYR ke PI")
            print("5. Keluar")
            
            try:
                choice = int(input("Masukkan pilihan (1-5): "))
                if choice == 5:
                    print("Terima kasih kerana menggunakan kalkulator!")
                    break
                if choice not in [1, 2, 3, 4]:
                    print("Sila pilih pilihan yang sah (1-5).")
                    continue
                
                amount = float(input("Masukkan jumlah: "))
                if amount < 0:
                    print("Sila masukkan jumlah positif.")
                    continue
                
                if choice == 1:
                    result = self.pi_to_usd(amount)
                    if result is not None:
                        print(f"{amount:.2f} PI = ${result:.2f} USD")
                    else:
                        print("Gagal mengira kerana data harga tidak tersedia.")
                elif choice == 2:
                    result = self.pi_to_myr(amount)
                    if result is not None:
                        print(f"{amount:.2f} PI = RM{result:.2f} MYR")
                    else:
                        print("Gagal mengira kerana data harga tidak tersedia.")
                elif choice == 3:
                    result = self.usd_to_pi(amount)
                    if result is not None:
                        print(f"${amount:.2f} USD = {result:.2f} PI")
                    else:
                        print("Gagal mengira kerana data harga tidak tersedia.")
                elif choice == 4:
                    result = self.myr_to_pi(amount)
                    if result is not None:
                        print(f"RM{amount:.2f} MYR = {result:.2f} PI")
                    else:
                        print("Gagal mengira kerana data harga tidak tersedia.")
                
            except ValueError:
                print("Sila masukkan nombor yang sah.")

if __name__ == "__main__":
    calculator = PiCalculator()
    calculator.run()