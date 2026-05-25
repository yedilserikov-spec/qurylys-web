import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#2B2B2B] text-white overflow-hidden">

      {/* HERO */}
      <section className="relative flex min-h-screen items-center justify-center px-6">

        {/* Glow effect */}
        <div className="absolute top-[-200px] left-1/2 h-[500px] w-[500px] -translate-x-1/2 rounded-full bg-[#2AFF00]/20 blur-3xl" />

        <div className="relative z-10 max-w-5xl text-center">

          {/* LOGO */}
          <div className="flex justify-center">
            <Image
              src="/logo.png"
              alt="Qurylys"
              width={420}
              height={420}
              priority
              className="w-[240px] md:w-[420px] object-contain"
            />
          </div>

          <p className="mx-auto mt-8 max-w-3xl text-lg leading-relaxed text-white/70 md:text-2xl">
            Цифровая платформа для строительства,
            услуг, техники, тендеров и заказов.
          </p>

          {/* STATUS */}
          <div className="mt-12">
            <p className="text-2xl font-bold text-[#2AFF00] md:text-3xl">
              Скоро запуск
            </p>

            <p className="mt-3 text-base text-white/50 md:text-lg">
              Сайт находится в разработке
            </p>
          </div>

        </div>
      </section>
    </main>
  );
}