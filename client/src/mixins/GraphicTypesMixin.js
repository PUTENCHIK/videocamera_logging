import { formatDate, firstToUpperCase } from '../utils/helpers';

import CamerasMixin from './CamerasMixin';
import ClassesMixin from './ClassesMixin';
import SnapshotsMixin from './SnapshotsMixin';

export default {
    mixins: [CamerasMixin, ClassesMixin, SnapshotsMixin],

    data() {
        return {
            source: null,
            chartOption: {}
        }
    },

    methods: {
        getTitleText() {
            if (this.source == null) {
                return "Выберите категорию и объект";
            } else {
                let result = "Статистика ";
                if (this.source.category == "camera") {
                    this.cameras.forEach((camera) => {
                        if (camera.id == this.source.id) {
                            result += `камеры #${camera.id}`;
                        }
                    });
                } else {
                    this.classes.forEach((class_) => {
                        if (class_.id == this.source.id) {
                            result += `класса '${firstToUpperCase(class_.title)}'`;
                        }
                    });
                }
                return result;
            }
        },

        getGrid() {
            return {
                left: 40,
                right: 40,
                bottom: 40,
                top: 80
            }
        },

        getTooltip() {
            return {
                trigger: 'item',
                formatter: (item) => {
                    let object = item.value[2];
                    return `
                        <b>${firstToUpperCase(object.trackable_class.title)}</b><br>
                        Добавлен: ${formatDate(object.created_at)}<br>
                        Вероятность: ${object.probability}<br>
                        ID снимка: ${object.snapshot_id}
                    `;
                }
            };
        },

        getToolbox() {
            return {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            };
        },

        getDatazoom() {
            return [
                {
                    type: 'inside',
                    start: 0,
                    end: 100
                },
                {
                    start: 0,
                    end: 100
                }
            ]
        },

        getData() {
            let data = [];
            if (this.source.category == "camera") {
                this.objects.forEach((object) => {
                    if (object.snapshot.camera_id == this.source.id) {
                        let date = new Date(object.created_at);
                        let image_name;
                        if (object.trackable_class) {
                            image_name = object.trackable_class.name;
                        } else {
                            image_name = "unknown";
                        }

                        data.push({
                            value: [date, object.probability, object],
                            symbol: `image:///src/assets/icons/${image_name}.png`,
                            symbolSize: 32,
                            symbolOffset: [0, 0],
                        });
                    }
                });
            }
            return data;
        },

        updateChartOption() {
            this.chartOption = {
                title: {
                    text: this.getTitleText(),
                    top: 20,
                    left: 'center',
                },
                grid: this.getGrid(),
                tooltip: this.getTooltip(),
                toolbox: this.getToolbox(),
                dataZoom: this.getDatazoom(),
                xAxis: {
                    type: 'time',
                    boundaryGap: false
                },
                yAxis: {
                    type: 'value',
                    boundaryGap: [0, '100%']
                },
                series: [
                    {
                        data: this.getData(),
                        type: 'scatter',
                    }
                ]
            };
        }
    },

    async mounted() {
        await this.loadCameras();
        await this.loadClasses();
        await this.loadSnapshots();
        await this.loadObjects();
    }
}