import { formatDate, firstToUpperCase } from '../utils/helpers';

import CamerasMixin from './CamerasMixin';
import ClassesMixin from './ClassesMixin';
import SnapshotsMixin from './SnapshotsMixin';

export default {
    mixins: [CamerasMixin, ClassesMixin, SnapshotsMixin],

    data() {
        return {
            source: null,
            chart_option: {},
            no_trackable_class_warning_shown: false
        }
    },

    methods: {
        getClassById(id) {
            for (let i = 0; i < this.classes.length; i++) {
                let class_ = this.classes[i];
                if (class_.id === id) {
                    return class_;
                }
            };
        },

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
                    let title = object.trackable_class ?
                        object.trackable_class.title : "неизвестный класс";
                    return `
                        <b>${firstToUpperCase(title)}</b><br>
                        Добавлен: ${formatDate(object.created_at)}<br>
                        Метка: ${object.label}<br>
                        Вероятность: ${object.probability}<br>
                        ID камеры: ${object.snapshot.camera_id}<br>
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

        getCamerasData() {
            let data = [];
            this.objects.forEach((object) => {
                if (object.snapshot.camera_id == this.source.id) {
                    let date = new Date(object.created_at);
                    let image_name;
                    if (object.trackable_class) {
                        image_name = object.trackable_class.name;
                    } else {
                        image_name = "unknown";
                        if (!this.no_trackable_class_warning_shown) {
                            this.addWarning("Неизвестный класс",
                                `В базе хранятся объекты с меткой ${object.label}, для которой не задан класс`);
                            this.no_trackable_class_warning_shown = true;
                        }
                    }

                    data.push({
                        value: [date, object.probability, object],
                        symbol: `image:///src/assets/icons/${image_name}.png`,
                        symbolSize: 32,
                        symbolOffset: [0, 0],
                    });
                }
            });
            return data;
        },

        getClassesData() {
            let data = [];
            this.objects.forEach((object) => {
                let tc = object.trackable_class;
                if (tc && tc.id == this.source.id) {
                    let date = new Date(object.created_at);
                    let image_name = tc.name;

                    data.push({
                        value: [date, object.probability, object],
                        symbol: `image:///src/assets/icons/${image_name}.png`,
                        symbolSize: 32,
                        symbolOffset: [0, 0],
                    });
                }
            });
            return data;
        },

        getData() {
            let data = [];
            if (this.source.category == "camera") {
                data = this.getCamerasData();
                if (!data.length) {
                    this.addWarning("Нет объектов",
                        `Для камеры #${this.source.id} не было сохранено ни одного объекта`
                    );
                }
            } else if (this.source.category == "class") {
                data = this.getClassesData();
                if (!data.length) {
                    let class_ = this.getClassById(this.source.id);
                    this.addWarning("Нет объектов",
                        `В базе нет ни одного объекта класса '${firstToUpperCase(class_.title)}'`
                    );
                }
            }
            
            return data;
        },

        updateChartOption() {
            this.chart_option = {
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