<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img src="assets/hero-dark.svg" width="100%" alt="An editor window with a Kotlin class that describes dec0iiyy: Android engineer and Rust contributor, Kotlin, Jetpack Compose, coroutines and Flow, MVI, Kotlin Multiplatform, networking in Rust. Next to it, a phone shows a list screen and exchanges packets with TLS, QUIC and DNS nodes.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=19&duration=2600&pause=1200&color=CBA6F7&center=true&vCenter=true&width=640&height=44&lines=Readable+Kotlin+over+clever+Kotlin;From+packets+to+pixels;One+state%2C+one+source+of+truth;Measure+first%2C+then+optimise">
  <source media="(prefers-color-scheme: light)" srcset="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=19&duration=2600&pause=1200&color=8839EF&center=true&vCenter=true&width=640&height=44&lines=Readable+Kotlin+over+clever+Kotlin;From+packets+to+pixels;One+state%2C+one+source+of+truth;Measure+first%2C+then+optimise">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=19&duration=2600&pause=1200&color=CBA6F7&center=true&vCenter=true&width=640&height=44&lines=Readable+Kotlin+over+clever+Kotlin;From+packets+to+pixels;One+state%2C+one+source+of+truth;Measure+first%2C+then+optimise" alt="Readable Kotlin over clever Kotlin. From packets to pixels. One state, one source of truth. Measure first, then optimise.">
</picture>

<br>

<img src="https://img.shields.io/badge/Android-engineer-a6e3a1?style=flat-square&labelColor=1e1e2e&logo=android&logoColor=a6e3a1" alt="Android engineer">
<img src="https://img.shields.io/badge/Kotlin-first-cba6f7?style=flat-square&labelColor=1e1e2e&logo=kotlin&logoColor=cba6f7" alt="Kotlin first">
<img src="https://img.shields.io/badge/Rust-networking-fab387?style=flat-square&labelColor=1e1e2e&logo=rust&logoColor=fab387" alt="Rust for networking">
<img src="https://img.shields.io/badge/in%20production-3%2B%20years-89b4fa?style=flat-square&labelColor=1e1e2e" alt="3+ years in production">
<img src="https://img.shields.io/badge/feature%20modules-25%20from%20scratch-94e2d5?style=flat-square&labelColor=1e1e2e" alt="25 feature modules built from scratch">
<img src="https://img.shields.io/badge/English-B2-f9e2af?style=flat-square&labelColor=1e1e2e" alt="English B2">

</div>

## About

I'm an Android engineer with more than three years of commercial Kotlin. I work in product teams, and the job runs from a single feature to the module structure a whole app stands on: so far I have built 25 feature modules from scratch. In the open, I contribute to networking code in Rust.

- 📱 **Android first.** Jetpack Compose and Material 3 on top of coroutines and Flow.
- 🧩 **Architecture.** MVI on Clean Architecture, multi-module, with one state per screen.
- 🌍 **Multiplatform.** Kotlin Multiplatform when Android and iOS should share one codebase.
- 🦀 **Networking in Rust.** TLS, QUIC and DNS on async I/O, with the JNI and FFI bridges that bring one core to Android and iOS.
- 🤝 **In a team.** Code review, technical interviews, Scrum.

## Stack

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=kotlin%2Candroidstudio%2Cgradle%2Cktor%2Csqlite%2Cfirebase%2Crust%2Cgit%2Cgithubactions%2Cfigma&theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=kotlin%2Candroidstudio%2Cgradle%2Cktor%2Csqlite%2Cfirebase%2Crust%2Cgit%2Cgithubactions%2Cfigma&theme=light">
    <img src="https://skillicons.dev/icons?i=kotlin%2Candroidstudio%2Cgradle%2Cktor%2Csqlite%2Cfirebase%2Crust%2Cgit%2Cgithubactions%2Cfigma&theme=dark" alt="Kotlin, Android Studio, Gradle, Ktor, SQLite, Firebase, Rust, Git, GitHub Actions, Figma">
  </picture>
</p>

| Area | What I use |
| :-- | :-- |
| **Languages** | Kotlin, Rust |
| **UI** | Jetpack Compose, Material 3, Navigation |
| **Concurrency** | Coroutines, Flow |
| **Architecture** | MVI, Clean Architecture, multi-module, Kotlin Multiplatform |
| **Data** | Room, Retrofit, Ktor |
| **Dependency injection** | Koin |
| **Networking** | Rust with Tokio: TLS, QUIC, DNS |
| **Build and quality** | Gradle convention plugins, detekt, R8, GitHub Actions |

## How I build

```mermaid
flowchart LR
    subgraph ui["UI · Jetpack Compose"]
        screen["Screen"] -- "action" --> vm["ViewModel"]
        vm -- "state" --> screen
    end
    subgraph domain["Domain · pure Kotlin"]
        usecase["Use cases"]
    end
    subgraph data["Data"]
        repo["Repositories"] --> api[("Network")]
        repo --> db[("Database")]
    end
    vm --> usecase --> repo
```

- **One direction.** A screen sends actions and renders one immutable state.
- **Small modules.** A feature sits behind a thin API module, so builds stay fast and boundaries stay honest.
- **Build logic as code.** Convention plugins, detekt and R8 rules live next to the app and are reviewed like it.

## GitHub activity

> [!NOTE]
> Most of my Kotlin lives in private product repositories. What you see here is only the part I do in the open.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dec0iiyy/dec0iiyy/output/activity-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dec0iiyy/dec0iiyy/output/activity-light.svg">
    <img src="https://raw.githubusercontent.com/dec0iiyy/dec0iiyy/output/activity-dark.svg" width="100%" alt="My last 30 days on GitHub: contributions per day, with totals for commits, pull requests, reviews and issues, and the pull requests merged in open source so far">
  </picture>
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&height=110&section=footer&color=0:7F52FF,50:C711E1,100:E44857" width="100%" alt="">
