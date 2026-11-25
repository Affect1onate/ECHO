"""Reproduce the three-pipeline, seven-method scaling figure.

Usage: python plot_sample_size_scaling.py
       python plot_sample_size_scaling.py --output-dir ./figures
Dependency: matplotlib (pip install matplotlib)

Measured results are embedded; no external data or model calls are needed.
Outputs: sample_size_scaling_asr.png and sample_size_scaling_asr.pdf.
The screenshot's viewer border is not part of the scientific figure.
"""

from pathlib import Path
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIZES = [160, 320, 640, 1280, 2244]
PIPELINES = [
    ("e5-mistral", "E5-Mistral → Gemma"),
    ("colbertv2", "ColBERTv2 → Vicuna"),
    ("bm25", "BM25 → Gemma"),
]
# key, legend label, color, marker, line style
METHODS = [
    ("enhanced", "ECHO (ours)", "#c9302c", "o", "-"),
    ("chatinject_code", "ChatInject (single-turn)", "#3977b5", "s", "--"),
    ("corrupt_as", "CorruptRAG-AS-style", "#458b63", "^", "--"),
    ("fixed_topic", "LM-topic template", "#e6912b", "D", ":"),
    ("semantic_llm", "Semantic rewriting", "#8659a6", "v", "-."),
    ("hotflip_CS", "HotFlip + C+S", "#3aa5ae", "P", "--"),
    ("authchain_local", "AuthChain-style (local)", "#8b6656", "X", ":"),
]

# Each method stores ASR proportions and cumulative generation seconds,
# ordered by SIZES. Copied without rounding from the saved experiment report.
DATA = {'e5-mistral': {'enhanced': {'rate': [0.85625, 0.871875, 0.8875, 0.9015625, 0.9050802139037433],
                             'generation_seconds': [54.050794699986,
                                                    109.91164269996807,
                                                    208.5563633999409,
                                                    416.85675669995544,
                                                    726.1204705000855]},
                'chatinject_code': {'rate': [0.18125, 0.19375, 0.1828125, 0.18984375, 0.18538324420677363],
                                    'generation_seconds': [93.55750059997081,
                                                           190.97787819997757,
                                                           375.38122859994473,
                                                           743.6188147999637,
                                                           1315.1672843999258]},
                'corrupt_as': {'rate': [0.15625, 0.159375, 0.15, 0.15234375, 0.1483957219251337],
                               'generation_seconds': [101.94491910006036,
                                                      206.76462930004345,
                                                      406.0415853001323,
                                                      806.1914689000841,
                                                      1415.4805179000396]},
                'fixed_topic': {'rate': [0.13125, 0.125, 0.1203125, 0.12578125, 0.1270053475935829],
                                'generation_seconds': [107.71953420006321,
                                                       216.0347915001039,
                                                       428.9457104001194,
                                                       866.4354327001492,
                                                       1516.382991000166]},
                'semantic_llm': {'rate': [0.10625, 0.115625, 0.115625, 0.12421875, 0.12344028520499109],
                                 'generation_seconds': [105.33592360003968,
                                                        215.75870909995865,
                                                        433.2254791999003,
                                                        875.9674271999975,
                                                        1534.6149343998986]},
                'hotflip_CS': {'rate': [0.09375, 0.109375, 0.115625, 0.12578125, 0.12789661319073084],
                               'generation_seconds': [105.57362230005674,
                                                      218.87023500012583,
                                                      438.86525860015536,
                                                      874.1642101000762,
                                                      1528.8371350000089]},
                'authchain_local': {'rate': [0.1, 0.1125, 0.0953125, 0.0953125, 0.09046345811051694],
                                    'generation_seconds': [113.22411560005276,
                                                           228.45277930007433,
                                                           451.99647170008393,
                                                           904.3856865000562,
                                                           1583.9463636001456]}},
 'colbertv2': {'enhanced': {'rate': [0.775, 0.778125, 0.8109375, 0.8, 0.7896613190730838],
                            'generation_seconds': [85.522934800043,
                                                   170.5681048000406,
                                                   341.72714100008307,
                                                   684.2757622000645,
                                                   1190.1185191001277]},
               'chatinject_code': {'rate': [0.76875, 0.74375, 0.746875, 0.746875, 0.7468805704099821],
                                   'generation_seconds': [86.81334229998174,
                                                          174.1636513999838,
                                                          344.76910830001,
                                                          691.0880923000368,
                                                          1204.9707661999855]},
               'corrupt_as': {'rate': [0.4375, 0.434375, 0.4359375, 0.43203125, 0.42914438502673796],
                              'generation_seconds': [83.65895129999262,
                                                     168.2690094999707,
                                                     333.2409659999248,
                                                     667.095379999897,
                                                     1167.688094399855]},
               'fixed_topic': {'rate': [0.49375, 0.484375, 0.51875, 0.5328125, 0.535204991087344],
                               'generation_seconds': [92.8048204999941,
                                                      185.47473879990866,
                                                      368.7952949999308,
                                                      737.0626975000196,
                                                      1285.9682985999389]},
               'semantic_llm': {'rate': [0.39375, 0.396875, 0.39375, 0.396875, 0.39705882352941174],
                                'generation_seconds': [93.8332751999551,
                                                       187.28396099986276,
                                                       374.72364279985777,
                                                       749.6581429998623,
                                                       1306.5532290001283]},
               'hotflip_CS': {'rate': [0.36875, 0.36875, 0.3921875, 0.40390625, 0.40240641711229946],
                              'generation_seconds': [92.62511950003682,
                                                     186.27362570012338,
                                                     372.62420070020016,
                                                     744.2494617001794,
                                                     1302.9143425002403]},
               'authchain_local': {'rate': [0.3125, 0.309375, 0.3109375, 0.309375, 0.3088235294117647],
                                   'generation_seconds': [96.65494200002286,
                                                          196.31522639998002,
                                                          389.09399869979825,
                                                          778.5698508997448,
                                                          1359.8165822997107]}},
 'bm25': {'enhanced': {'rate': [0.8625, 0.871875, 0.865625, 0.88515625, 0.8770053475935828],
                       'generation_seconds': [52.61007459991379,
                                              106.3852221998095,
                                              212.85642479968374,
                                              426.5980772997136,
                                              742.1938780996716]},
          'chatinject_code': {'rate': [0.2, 0.2, 0.19375, 0.19921875, 0.19117647058823528],
                              'generation_seconds': [91.35029970001779,
                                                     180.9296522999939,
                                                     367.2256654999219,
                                                     728.4143920998322,
                                                     1293.9588206998887]},
          'corrupt_as': {'rate': [0.15625, 0.159375, 0.146875, 0.14765625, 0.14037433155080214],
                         'generation_seconds': [98.18091660001664,
                                                203.54798190004658,
                                                401.45350519998465,
                                                794.0432299000968,
                                                1403.9332688999712]},
          'fixed_topic': {'rate': [0.13125, 0.128125, 0.1203125, 0.11953125, 0.11452762923351159],
                          'generation_seconds': [105.49143870000262,
                                                 216.78861399996094,
                                                 425.1871108999767,
                                                 839.2654522998782,
                                                 1473.9042343996407]},
          'semantic_llm': {'rate': [0.13125, 0.140625, 0.1265625, 0.13515625, 0.12789661319073084],
                           'generation_seconds': [103.54026879995945,
                                                  216.33013919991208,
                                                  428.63743679993786,
                                                  860.1854965999373,
                                                  1516.7579775997729]},
          'hotflip_CS': {'rate': [0.15625, 0.146875, 0.1359375, 0.1375, 0.12967914438502673],
                         'generation_seconds': [104.79449050003313,
                                                218.7988827000081,
                                                432.9645450999087,
                                                861.9947373999748,
                                                1500.2958732001425]},
          'authchain_local': {'rate': [0.11875, 0.10625, 0.0890625, 0.09609375, 0.0944741532976827],
                              'generation_seconds': [110.54042569999001,
                                                     227.24900369998068,
                                                     449.91142019996187,
                                                     896.0355819998658,
                                                     1568.0996396998235]}}}


def plot(output_dir: Path) -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    fig, axes = plt.subplots(
        2, 3, figsize=(12.45, 6.6), sharex=True,
        layout="constrained", squeeze=False,
    )
    for column, (retriever, title) in enumerate(PIPELINES):
        for key, label, color, marker, style in METHODS:
            series = DATA[retriever][key]
            for row, metric, scale in [
                (0, "rate", 100), (1, "generation_seconds", 1 / 60)
            ]:
                axes[row, column].plot(
                    SIZES, [value * scale for value in series[metric]],
                    color=color, marker=marker, linestyle=style,
                    linewidth=2.2 if key == "enhanced" else 1.3,
                    markersize=5 if key == "enhanced" else 4,
                    label=label, zorder=10 if key == "enhanced" else 3,
                )
        axes[0, column].set_title(f"({chr(97 + column)}) {title}")
        axes[0, column].set_ylim(0, 100)
        axes[1, column].set_ylim(bottom=0)
        axes[1, column].set_xlabel("Number of test queries")
        for ax in axes[:, column]:
            ax.grid(True, linestyle=":", alpha=0.4)
            ax.set_xticks(SIZES, ["160", "320", "640", "1,280", "2,244"], rotation=30)
            ax.tick_params(labelsize=9)
    axes[0, 0].set_ylabel("Attack success rate (%)")
    axes[1, 0].set_ylabel("Cumulative generation time (min)")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="outside upper center", ncol=4,
               frameon=False, fontsize=9)
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "pdf"):
        path = output_dir / f"sample_size_scaling_asr.{extension}"
        fig.savefig(path, facecolor="white")
        print(path.resolve())
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    plot(args.output_dir)
